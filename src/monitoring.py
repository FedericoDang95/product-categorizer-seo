"""Sistema di monitoraggio e metriche per l'API"""

import time
import logging
from typing import Dict, Any, Optional
from functools import wraps
from collections import defaultdict, deque
from datetime import datetime, timedelta
import threading
import json

class MetricsCollector:
    """Raccoglie e gestisce metriche dell'applicazione"""
    
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self.metrics = {
            'requests': defaultdict(int),
            'response_times': defaultdict(list),
            'errors': defaultdict(int),
            'categorizations': defaultdict(int),
            'cache_hits': 0,
            'cache_misses': 0
        }
        self.request_history = deque(maxlen=max_history)
        self.error_history = deque(maxlen=max_history)
        self._lock = threading.Lock()
        self.start_time = datetime.now()
        
    def record_request(self, endpoint: str, method: str, response_time: float, 
                      status_code: int, user_ip: str = None):
        """Registra una richiesta API"""
        with self._lock:
            key = f"{method}:{endpoint}"
            self.metrics['requests'][key] += 1
            self.metrics['response_times'][key].append(response_time)
            
            # Mantieni solo gli ultimi N tempi di risposta
            if len(self.metrics['response_times'][key]) > 100:
                self.metrics['response_times'][key] = self.metrics['response_times'][key][-100:]
            
            # Registra errori
            if status_code >= 400:
                self.metrics['errors'][key] += 1
                self.error_history.append({
                    'timestamp': datetime.now().isoformat(),
                    'endpoint': endpoint,
                    'method': method,
                    'status_code': status_code,
                    'user_ip': user_ip,
                    'response_time': response_time
                })
            
            # Aggiungi alla cronologia
            self.request_history.append({
                'timestamp': datetime.now().isoformat(),
                'endpoint': endpoint,
                'method': method,
                'response_time': response_time,
                'status_code': status_code,
                'user_ip': user_ip
            })
    
    def record_categorization(self, category: str, confidence: float, 
                            processing_time: float, is_new_category: bool = False):
        """Registra una categorizzazione"""
        with self._lock:
            self.metrics['categorizations'][category] += 1
            
            # Metriche specifiche per categorizzazione
            if not hasattr(self, 'categorization_metrics'):
                self.categorization_metrics = {
                    'total_categorizations': 0,
                    'avg_confidence': 0,
                    'avg_processing_time': 0,
                    'new_categories_created': 0,
                    'confidence_distribution': defaultdict(int)
                }
            
            self.categorization_metrics['total_categorizations'] += 1
            
            # Aggiorna media confidence
            total = self.categorization_metrics['total_categorizations']
            current_avg = self.categorization_metrics['avg_confidence']
            self.categorization_metrics['avg_confidence'] = (
                (current_avg * (total - 1) + confidence) / total
            )
            
            # Aggiorna media processing time
            current_avg_time = self.categorization_metrics['avg_processing_time']
            self.categorization_metrics['avg_processing_time'] = (
                (current_avg_time * (total - 1) + processing_time) / total
            )
            
            if is_new_category:
                self.categorization_metrics['new_categories_created'] += 1
            
            # Distribuzione confidence
            confidence_bucket = int(confidence * 10) / 10  # Arrotonda a 0.1
            self.categorization_metrics['confidence_distribution'][confidence_bucket] += 1
    
    def record_cache_hit(self):
        """Registra un cache hit"""
        with self._lock:
            self.metrics['cache_hits'] += 1
    
    def record_cache_miss(self):
        """Registra un cache miss"""
        with self._lock:
            self.metrics['cache_misses'] += 1
    
    def get_summary(self) -> Dict[str, Any]:
        """Restituisce un riassunto delle metriche"""
        with self._lock:
            uptime = datetime.now() - self.start_time
            
            # Calcola statistiche sui tempi di risposta
            avg_response_times = {}
            for endpoint, times in self.metrics['response_times'].items():
                if times:
                    avg_response_times[endpoint] = {
                        'avg': sum(times) / len(times),
                        'min': min(times),
                        'max': max(times),
                        'count': len(times)
                    }
            
            # Calcola tasso di errore
            error_rates = {}
            for endpoint in self.metrics['requests']:
                total_requests = self.metrics['requests'][endpoint]
                total_errors = self.metrics['errors'][endpoint]
                error_rates[endpoint] = {
                    'total_requests': total_requests,
                    'total_errors': total_errors,
                    'error_rate': (total_errors / total_requests * 100) if total_requests > 0 else 0
                }
            
            # Cache statistics
            total_cache_ops = self.metrics['cache_hits'] + self.metrics['cache_misses']
            cache_hit_rate = (
                (self.metrics['cache_hits'] / total_cache_ops * 100) 
                if total_cache_ops > 0 else 0
            )
            
            summary = {
                'uptime_seconds': uptime.total_seconds(),
                'uptime_human': str(uptime),
                'total_requests': sum(self.metrics['requests'].values()),
                'total_errors': sum(self.metrics['errors'].values()),
                'avg_response_times': avg_response_times,
                'error_rates': error_rates,
                'cache_hit_rate': cache_hit_rate,
                'cache_stats': {
                    'hits': self.metrics['cache_hits'],
                    'misses': self.metrics['cache_misses'],
                    'hit_rate': cache_hit_rate
                },
                'top_categories': dict(
                    sorted(self.metrics['categorizations'].items(), 
                          key=lambda x: x[1], reverse=True)[:10]
                )
            }
            
            # Aggiungi metriche di categorizzazione se disponibili
            if hasattr(self, 'categorization_metrics'):
                summary['categorization_stats'] = self.categorization_metrics.copy()
            
            return summary
    
    def get_recent_errors(self, limit: int = 10) -> list:
        """Restituisce gli errori più recenti"""
        with self._lock:
            return list(self.error_history)[-limit:]
    
    def get_health_status(self) -> Dict[str, Any]:
        """Restituisce lo stato di salute del sistema"""
        with self._lock:
            summary = self.get_summary()
            
            # Determina lo stato di salute
            health_status = "healthy"
            issues = []
            
            # Controlla tasso di errore
            for endpoint, stats in summary['error_rates'].items():
                if stats['error_rate'] > 10:  # Più del 10% di errori
                    health_status = "degraded"
                    issues.append(f"Alto tasso di errore per {endpoint}: {stats['error_rate']:.1f}%")
                elif stats['error_rate'] > 25:  # Più del 25% di errori
                    health_status = "unhealthy"
            
            # Controlla tempi di risposta
            for endpoint, stats in summary['avg_response_times'].items():
                if stats['avg'] > 5.0:  # Più di 5 secondi
                    if health_status == "healthy":
                        health_status = "degraded"
                    issues.append(f"Tempi di risposta lenti per {endpoint}: {stats['avg']:.2f}s")
            
            # Controlla cache hit rate
            if summary['cache_hit_rate'] < 50 and summary['cache_stats']['hits'] + summary['cache_stats']['misses'] > 100:
                if health_status == "healthy":
                    health_status = "degraded"
                issues.append(f"Basso cache hit rate: {summary['cache_hit_rate']:.1f}%")
            
            return {
                'status': health_status,
                'timestamp': datetime.now().isoformat(),
                'uptime': summary['uptime_human'],
                'issues': issues,
                'metrics_summary': {
                    'total_requests': summary['total_requests'],
                    'total_errors': summary['total_errors'],
                    'cache_hit_rate': summary['cache_hit_rate']
                }
            }

# Istanza globale del collector
metrics_collector = MetricsCollector()

def monitor_performance(endpoint_name: str = None):
    """Decorator per monitorare le performance degli endpoint"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            endpoint = endpoint_name or func.__name__
            
            try:
                # Esegui la funzione
                result = func(*args, **kwargs)
                
                # Calcola tempo di risposta
                response_time = time.time() - start_time
                
                # Determina status code dalla risposta
                status_code = 200
                if hasattr(result, 'status_code'):
                    status_code = result.status_code
                elif isinstance(result, tuple) and len(result) > 1:
                    status_code = result[1]
                
                # Registra metriche
                metrics_collector.record_request(
                    endpoint=endpoint,
                    method='POST',  # Assumiamo POST per la maggior parte degli endpoint
                    response_time=response_time,
                    status_code=status_code
                )
                
                return result
                
            except Exception as e:
                # Registra errore
                response_time = time.time() - start_time
                metrics_collector.record_request(
                    endpoint=endpoint,
                    method='POST',
                    response_time=response_time,
                    status_code=500
                )
                raise
        
        return wrapper
    return decorator

class PerformanceLogger:
    """Logger specializzato per performance"""
    
    def __init__(self, name: str = "performance"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Crea handler se non esiste
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def log_categorization(self, title: str, category: str, confidence: float, 
                          processing_time: float, is_new_category: bool = False):
        """Log di una categorizzazione"""
        self.logger.info(
            f"CATEGORIZATION - Title: {title[:50]}... | "
            f"Category: {category} | Confidence: {confidence:.3f} | "
            f"Time: {processing_time:.3f}s | New: {is_new_category}"
        )
        
        # Registra anche nelle metriche
        metrics_collector.record_categorization(
            category=category,
            confidence=confidence,
            processing_time=processing_time,
            is_new_category=is_new_category
        )
    
    def log_batch_processing(self, batch_size: int, successful: int, 
                           total_time: float, batch_id: str = None):
        """Log di elaborazione batch"""
        success_rate = (successful / batch_size * 100) if batch_size > 0 else 0
        avg_time_per_item = total_time / batch_size if batch_size > 0 else 0
        
        self.logger.info(
            f"BATCH_PROCESSING - ID: {batch_id or 'N/A'} | "
            f"Size: {batch_size} | Successful: {successful} | "
            f"Success Rate: {success_rate:.1f}% | "
            f"Total Time: {total_time:.3f}s | "
            f"Avg Time/Item: {avg_time_per_item:.3f}s"
        )
    
    def log_cache_operation(self, operation: str, key: str, hit: bool = None):
        """Log di operazioni cache"""
        if hit is not None:
            result = "HIT" if hit else "MISS"
            self.logger.debug(f"CACHE_{result} - Operation: {operation} | Key: {key[:50]}...")
            
            if hit:
                metrics_collector.record_cache_hit()
            else:
                metrics_collector.record_cache_miss()
        else:
            self.logger.debug(f"CACHE_OPERATION - Operation: {operation} | Key: {key[:50]}...")
    
    def log_error(self, operation: str, error: Exception, context: Dict[str, Any] = None):
        """Log di errori con contesto"""
        context_str = ""
        if context:
            context_str = f" | Context: {json.dumps(context, default=str)}"
        
        self.logger.error(
            f"ERROR - Operation: {operation} | "
            f"Error: {type(error).__name__}: {str(error)}{context_str}"
        )

# Istanza globale del performance logger
performance_logger = PerformanceLogger()