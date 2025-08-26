from dataclasses import dataclass, field
from typing import Dict, List, Any

@dataclass
class CriticInsightMerger:
    def weight_feedback(self, feedback_items):
        return feedback_items
<<<<<<< HEAD
    def synthesize_arguments(self, weighted_feedback):
        return {"combined_argument": "synthesized", "max_severity": "low"}
=======

    def synthesize_arguments(self, weighted_feedback):
        max_sev = "low"
        for item in weighted_feedback:
            sev = getattr(item, "severity", "low")
            if sev in ("high", "critical"):
                max_sev = "high"
                break
        return {"combined_argument": "synthesized", "max_severity": max_sev}
>>>>>>> 90775caae0ee1f419403e60a66426822b7ba0ef6

@dataclass
class PerformanceTracker:
    metrics: Dict[str, Any] = field(default_factory=dict)
    def record_event(self, event_type: str, success: bool, attempt: int = 1):
        if "retry_attempts" not in self.metrics:
            self.metrics["retry_attempts"] = 0
        if success:
            pass
        else:
            self.metrics["retry_attempts"] +=1
