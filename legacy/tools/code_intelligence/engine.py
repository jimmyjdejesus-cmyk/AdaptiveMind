"""
Code Intelligence Engine
Provides the core functionality for code analysis and completion using local Ollama models.
Enhanced with User Experience features for Issue #30.
"""

import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime


class CodeIntelligenceEngine:
    """Main engine for code analysis and intelligent completions with personalization."""
    
    def __init__(self):
        """Initialize the code intelligence engine."""
        self.completion_cache = {}
        self.feedback_history = []
    
    def get_personalized_completion(self, file_path: str, cursor_line: int, cursor_column: int, 
                                  model: str, username: str = "anonymous") -> List[Dict[str, Any]]:
        """Get personalized code completion suggestions."""
        try:
            # Import personalization components
            from agent.adapters.personalization_memory import get_user_personalization_memory, enhance_completion_with_personalization
            from database import get_user_preferences
            
            # Get user preferences and memory
            user_prefs = get_user_preferences(username)
            user_memory = get_user_personalization_memory(username)
            
            # Generate basic completions (mock implementation for now)
            basic_completions = self._generate_basic_completions(file_path, cursor_line, cursor_column, model)
            
            # Enhance completions with personalization
            enhanced_completions = []
            for completion in basic_completions:
                enhanced = enhance_completion_with_personalization(completion, user_prefs, user_memory)
                enhanced_completions.append(enhanced)
            
            return enhanced_completions
            
        except Exception as e:
            # Fallback to basic completions if personalization fails
            return self._generate_basic_completions(file_path, cursor_line, cursor_column, model)
    
    def _generate_basic_completions(self, file_path: str, cursor_line: int, cursor_column: int, 
                                   model: str) -> List[Dict[str, Any]]:
        """Generate basic code completions (mock implementation)."""
        # This is a mock implementation for demonstration
        # In real implementation, this would use Ollama/LLM to generate completions
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
        # Mock completions based on file type
        mock_completions = []
        
        if file_ext == '.py':
            mock_completions = [
                {
                    "suggestion": "def process_data(self, data):\n    return data.strip().lower()",
                    "confidence": 0.85,
                    "type": "method_completion"
                },
                {
                    "suggestion": "import pandas as pd",
                    "confidence": 0.75,
                    "type": "import_statement"
                }
            ]
        elif file_ext in ['.js', '.jsx']:
            mock_completions = [
                {
                    "suggestion": "const handleClick = () => {\n  setActive(!active);\n};",
                    "confidence": 0.80,
                    "type": "function_completion"
                }
            ]
        else:
            mock_completions = [
                {
                    "suggestion": "// TODO: Implement functionality",
                    "confidence": 0.60,
                    "type": "comment"
                }
            ]
        
        return mock_completions
    
    def record_personalized_feedback(self, file_path: str, cursor_line: int, cursor_column: int,
                                   suggestion: str, accepted: bool, username: str = "anonymous") -> bool:
        """Record user feedback with personalization learning."""
        try:
            # Import personalization components
            from agent.adapters.personalization_memory import get_user_personalization_memory
            from database import get_user_preferences
            
            # Get user preferences and memory
            user_prefs = get_user_preferences(username)
            user_memory = get_user_personalization_memory(username)
            
            # Create feedback context
            file_ext = os.path.splitext(file_path)[1].lower()
            context = {
                "file_type": file_ext,
                "file_path": file_path,
                "cursor_position": f"{cursor_line}:{cursor_column}",
                "suggestion_length": len(suggestion),
                "domain": user_prefs.get("domain_specialization", "General"),
                "pattern": "code_completion",
                "description": f"Code completion feedback for {file_ext} file"
            }
            
            # Record interaction for learning
            user_memory.record_interaction(
                interaction_type="code_completion",
                context=context,
                feedback=accepted,
                learning_rate=user_prefs.get("learning_rate", "Moderate")
            )
            
            # Store feedback in local history
            feedback_entry = {
                "timestamp": datetime.now().isoformat(),
                "file_path": file_path,
                "suggestion": suggestion,
                "accepted": accepted,
                "username": username,
                "context": context
            }
            self.feedback_history.append(feedback_entry)
            
            return True
            
        except Exception as e:
            # Don't fail if personalization recording fails
            return True


def get_code_completion(file_path, cursor_line, cursor_column, model, username="anonymous"):
    """Get code completion suggestions for a specific position in a file."""
    engine = CodeIntelligenceEngine()
    return engine.get_personalized_completion(file_path, cursor_line, cursor_column, model, username)


def record_completion_feedback(file_path, cursor_line, cursor_column, suggestion, accepted, username="anonymous"):
    """Record user feedback on a completion suggestion."""
    engine = CodeIntelligenceEngine()
    return engine.record_personalized_feedback(file_path, cursor_line, cursor_column, suggestion, accepted, username)
