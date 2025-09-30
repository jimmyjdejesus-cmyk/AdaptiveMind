"""Bridge between new security systems and legacy security."""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class SecurityBridge:
    """Bridge between new security systems and legacy security."""
    
    def __init__(self, new_agent_manager=None):
        """Initialize the security bridge.
        
        Args:
            new_agent_manager: New AgentManager instance
        """
        self.new_agent_manager = new_agent_manager
        self.security_events = []
    
    def validate_agent_action(self, agent_id: str, action: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate an agent action using new security systems."""
        try:
            # Get agent from new system
            if not self.new_agent_manager:
                return {"valid": True, "reason": "No new security system available"}
            
            agent = self.new_agent_manager.get_agent(agent_id)
            if not agent:
                return {"valid": False, "reason": "Agent not found"}
            
            # Basic security checks
            security_result = {
                "valid": True,
                "agent_id": agent_id,
                "action": action,
                "timestamp": datetime.now().isoformat(),
                "checks": []
            }
            
            # Check agent status
            status = self.new_agent_manager.get_agent_status(agent_id)
            if status and status.value == "error":
                security_result["valid"] = False
                security_result["reason"] = "Agent in error state"
                security_result["checks"].append("agent_status_check")
            
            # Check for suspicious actions
            suspicious_actions = ["delete", "remove", "destroy", "overwrite"]
            if any(suspicious in action.lower() for suspicious in suspicious_actions):
                security_result["checks"].append("suspicious_action_check")
                # In a real implementation, this would trigger additional validation
            
            # Check context for sensitive data
            sensitive_keys = ["password", "secret", "key", "token", "credential"]
            if any(key in str(context).lower() for key in sensitive_keys):
                security_result["checks"].append("sensitive_data_check")
                # In a real implementation, this would trigger additional validation
            
            # Log security event
            self.security_events.append(security_result)
            
            return security_result
            
        except Exception as e:
            logger.error(f"Security validation failed: {e}")
            return {
                "valid": False,
                "reason": f"Security validation error: {e}",
                "agent_id": agent_id,
                "action": action
            }
    
    def get_security_events(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent security events."""
        return self.security_events[-limit:]
    
    def get_security_stats(self) -> Dict[str, Any]:
        """Get security statistics."""
        total_events = len(self.security_events)
        valid_actions = sum(1 for event in self.security_events if event.get("valid", False))
        invalid_actions = total_events - valid_actions
        
        return {
            "total_events": total_events,
            "valid_actions": valid_actions,
            "invalid_actions": invalid_actions,
            "security_rate": valid_actions / total_events if total_events > 0 else 1.0,
            "bridge_available": self.new_agent_manager is not None
        }
    
    def run_security_audit(self) -> Dict[str, Any]:
        """Run a comprehensive security audit."""
        audit_result = {
            "timestamp": datetime.now().isoformat(),
            "checks": [],
            "issues": [],
            "recommendations": []
        }
        
        try:
            # Check agent manager availability
            if not self.new_agent_manager:
                audit_result["issues"].append("New security system not available")
                audit_result["recommendations"].append("Initialize new agent manager")
            else:
                audit_result["checks"].append("agent_manager_available")
            
            # Check agent security status
            if self.new_agent_manager:
                agents = list(self.new_agent_manager.agents.keys())
                error_agents = []
                
                for agent_id in agents:
                    status = self.new_agent_manager.get_agent_status(agent_id)
                    if status and status.value == "error":
                        error_agents.append(agent_id)
                
                if error_agents:
                    audit_result["issues"].append(f"Agents in error state: {error_agents}")
                    audit_result["recommendations"].append("Investigate and fix error agents")
                else:
                    audit_result["checks"].append("all_agents_healthy")
            
            # Check recent security events
            recent_events = self.get_security_events(50)
            invalid_events = [e for e in recent_events if not e.get("valid", True)]
            
            if invalid_events:
                audit_result["issues"].append(f"Recent invalid actions: {len(invalid_events)}")
                audit_result["recommendations"].append("Review and investigate invalid actions")
            else:
                audit_result["checks"].append("no_recent_invalid_actions")
            
            # Overall security score
            total_checks = len(audit_result["checks"])
            total_issues = len(audit_result["issues"])
            security_score = (total_checks - total_issues) / max(total_checks, 1)
            
            audit_result["security_score"] = security_score
            audit_result["status"] = "good" if security_score > 0.8 else "warning" if security_score > 0.5 else "critical"
            
        except Exception as e:
            logger.error(f"Security audit failed: {e}")
            audit_result["issues"].append(f"Audit error: {e}")
            audit_result["status"] = "error"
        
        return audit_result

# Global security bridge instance
security_bridge = None

def initialize_security_bridge(new_agent_manager=None):
    """Initialize the global security bridge."""
    global security_bridge
    security_bridge = SecurityBridge(new_agent_manager)
    return security_bridge

def get_security_bridge() -> Optional[SecurityBridge]:
    """Get the global security bridge instance."""
    return security_bridge
