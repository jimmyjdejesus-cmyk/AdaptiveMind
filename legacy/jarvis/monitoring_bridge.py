"""Bridge between new monitoring systems and legacy monitoring."""

import logging
import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class SystemMetric:
    """System metric data point."""
    name: str
    value: float
    unit: str
    timestamp: float
    tags: Dict[str, str] = None

class MonitoringBridge:
    """Bridge between new monitoring systems and legacy monitoring."""
    
    def __init__(self, new_agent_manager=None, new_ollama_client=None):
        """Initialize the monitoring bridge.
        
        Args:
            new_agent_manager: New AgentManager instance
            new_ollama_client: New OllamaClient instance
        """
        self.new_agent_manager = new_agent_manager
        self.new_ollama_client = new_ollama_client
        self.metrics_history = []
        self.max_history = 1000
    
    def collect_system_metrics(self) -> List[SystemMetric]:
        """Collect system metrics from all available sources."""
        metrics = []
        current_time = time.time()
        
        try:
            # Agent manager metrics
            if self.new_agent_manager:
                agent_metrics = self.new_agent_manager.get_metrics()
                
                for key, value in agent_metrics.items():
                    if isinstance(value, (int, float)):
                        metrics.append(SystemMetric(
                            name=f"agent_manager.{key}",
                            value=float(value),
                            unit="count" if "count" in key else "number",
                            timestamp=current_time,
                            tags={"source": "agent_manager"}
                        ))
            
            # Ollama client metrics
            if self.new_ollama_client:
                # Check Ollama health
                is_healthy = self.new_ollama_client.health_check()
                metrics.append(SystemMetric(
                    name="ollama.health",
                    value=1.0 if is_healthy else 0.0,
                    unit="boolean",
                    timestamp=current_time,
                    tags={"source": "ollama_client"}
                ))
                
                # Get available models count
                try:
                    models = self.new_ollama_client.get_available_models()
                    metrics.append(SystemMetric(
                        name="ollama.models_count",
                        value=float(len(models)),
                        unit="count",
                        timestamp=current_time,
                        tags={"source": "ollama_client"}
                    ))
                except Exception:
                    pass
            
            # System metrics (simplified)
            import psutil
            metrics.append(SystemMetric(
                name="system.cpu_percent",
                value=psutil.cpu_percent(),
                unit="percent",
                timestamp=current_time,
                tags={"source": "system"}
            ))
            
            metrics.append(SystemMetric(
                name="system.memory_percent",
                value=psutil.virtual_memory().percent,
                unit="percent",
                timestamp=current_time,
                tags={"source": "system"}
            ))
            
            # Store metrics in history
            self.metrics_history.extend(metrics)
            if len(self.metrics_history) > self.max_history:
                self.metrics_history = self.metrics_history[-self.max_history:]
            
        except Exception as e:
            logger.error(f"Failed to collect metrics: {e}")
        
        return metrics
    
    def get_metrics_summary(self, time_window_minutes: int = 60) -> Dict[str, Any]:
        """Get metrics summary for the specified time window."""
        cutoff_time = time.time() - (time_window_minutes * 60)
        recent_metrics = [m for m in self.metrics_history if m.timestamp >= cutoff_time]
        
        if not recent_metrics:
            return {"error": "No metrics available"}
        
        # Group metrics by name
        metrics_by_name = {}
        for metric in recent_metrics:
            if metric.name not in metrics_by_name:
                metrics_by_name[metric.name] = []
            metrics_by_name[metric.name].append(metric.value)
        
        # Calculate summaries
        summary = {
            "time_window_minutes": time_window_minutes,
            "total_metrics": len(recent_metrics),
            "unique_metrics": len(metrics_by_name),
            "metrics": {}
        }
        
        for name, values in metrics_by_name.items():
            if values:
                summary["metrics"][name] = {
                    "count": len(values),
                    "min": min(values),
                    "max": max(values),
                    "avg": sum(values) / len(values),
                    "latest": values[-1]
                }
        
        return summary
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get overall system health status."""
        health = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "unknown",
            "components": {},
            "issues": [],
            "recommendations": []
        }
        
        try:
            # Check agent manager
            if self.new_agent_manager:
                agent_metrics = self.new_agent_manager.get_metrics()
                error_agents = agent_metrics.get("error_agents", 0)
                
                if error_agents > 0:
                    health["components"]["agent_manager"] = "warning"
                    health["issues"].append(f"{error_agents} agents in error state")
                else:
                    health["components"]["agent_manager"] = "healthy"
            else:
                health["components"]["agent_manager"] = "unavailable"
                health["issues"].append("Agent manager not available")
            
            # Check Ollama client
            if self.new_ollama_client:
                is_healthy = self.new_ollama_client.health_check()
                if is_healthy:
                    health["components"]["ollama"] = "healthy"
                else:
                    health["components"]["ollama"] = "unavailable"
                    health["issues"].append("Ollama client not healthy")
            else:
                health["components"]["ollama"] = "unavailable"
                health["issues"].append("Ollama client not available")
            
            # Check system resources
            try:
                import psutil
                cpu_percent = psutil.cpu_percent()
                memory_percent = psutil.virtual_memory().percent
                
                if cpu_percent > 90:
                    health["issues"].append(f"High CPU usage: {cpu_percent}%")
                    health["recommendations"].append("Consider reducing concurrent operations")
                else:
                    health["components"]["cpu"] = "healthy"
                
                if memory_percent > 90:
                    health["issues"].append(f"High memory usage: {memory_percent}%")
                    health["recommendations"].append("Consider increasing memory or reducing memory usage")
                else:
                    health["components"]["memory"] = "healthy"
                    
            except ImportError:
                health["components"]["system"] = "psutil_not_available"
            
            # Determine overall status
            component_statuses = list(health["components"].values())
            if "unavailable" in component_statuses:
                health["overall_status"] = "critical"
            elif "warning" in component_statuses:
                health["overall_status"] = "warning"
            elif all(status == "healthy" for status in component_statuses):
                health["overall_status"] = "healthy"
            else:
                health["overall_status"] = "unknown"
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            health["overall_status"] = "error"
            health["issues"].append(f"Health check error: {e}")
        
        return health
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics and trends."""
        if not self.metrics_history:
            return {"error": "No metrics history available"}
        
        # Get recent metrics (last hour)
        recent_metrics = [m for m in self.metrics_history if m.timestamp >= time.time() - 3600]
        
        performance = {
            "timestamp": datetime.now().isoformat(),
            "metrics_count": len(recent_metrics),
            "trends": {}
        }
        
        # Analyze trends for key metrics
        key_metrics = ["agent_manager.tasks_completed", "agent_manager.active_agents", "ollama.health"]
        
        for metric_name in key_metrics:
            metric_values = [m.value for m in recent_metrics if m.name == metric_name]
            if metric_values:
                # Simple trend analysis
                if len(metric_values) > 1:
                    trend = "increasing" if metric_values[-1] > metric_values[0] else "decreasing"
                else:
                    trend = "stable"
                
                performance["trends"][metric_name] = {
                    "current": metric_values[-1],
                    "trend": trend,
                    "data_points": len(metric_values)
                }
        
        return performance
    
    def export_metrics(self, format: str = "json") -> Dict[str, Any]:
        """Export metrics in specified format."""
        if format == "json":
            return {
                "metrics": [
                    {
                        "name": m.name,
                        "value": m.value,
                        "unit": m.unit,
                        "timestamp": m.timestamp,
                        "tags": m.tags or {}
                    }
                    for m in self.metrics_history
                ],
                "export_timestamp": datetime.now().isoformat(),
                "total_metrics": len(self.metrics_history)
            }
        else:
            return {"error": f"Unsupported format: {format}"}

# Global monitoring bridge instance
monitoring_bridge = None

def initialize_monitoring_bridge(new_agent_manager=None, new_ollama_client=None):
    """Initialize the global monitoring bridge."""
    global monitoring_bridge
    monitoring_bridge = MonitoringBridge(new_agent_manager, new_ollama_client)
    return monitoring_bridge

def get_monitoring_bridge() -> Optional[MonitoringBridge]:
    """Get the global monitoring bridge instance."""
    return monitoring_bridge
