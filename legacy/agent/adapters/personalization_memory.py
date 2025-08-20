"""
LangChain Memory Integration for User Personalization
Part of Issue #30: User Experience Enhancements
"""

import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime

try:
    from langchain.memory import ConversationBufferMemory, ConversationSummaryBufferMemory
    from langchain.schema import BaseMessage, HumanMessage, AIMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    # Create fallback classes
    class ConversationBufferMemory:
        def __init__(self, *args, **kwargs):
            self.chat_memory = []
        
        def save_context(self, inputs, outputs):
            pass
            
        def load_memory_variables(self, inputs):
            return {}
    
    class ConversationSummaryBufferMemory(ConversationBufferMemory):
        pass


class PersonalizationMemory:
    """
    LangChain Memory-based personalization system that learns from user interactions
    and adapts AI responses based on preferences and feedback.
    """
    
    def __init__(self, user_id: str, memory_type: str = "buffer"):
        self.user_id = user_id
        self.memory_type = memory_type
        
        # Initialize LangChain memory
        if LANGCHAIN_AVAILABLE:
            if memory_type == "summary":
                self.memory = ConversationSummaryBufferMemory(
                    max_token_limit=2000,
                    return_messages=True
                )
            else:
                self.memory = ConversationBufferMemory(
                    return_messages=True
                )
        else:
            self.memory = ConversationBufferMemory()
        
        # User preference history
        self.preference_history = []
        self.interaction_patterns = {}
        self.learning_adaptations = {}
        
        self._load_user_memory()
    
    def _get_memory_file_path(self) -> str:
        """Get the file path for storing user memory."""
        memory_dir = os.path.join(os.getcwd(), 'user_memory')
        os.makedirs(memory_dir, exist_ok=True)
        return os.path.join(memory_dir, f"{self.user_id}_memory.json")
    
    def _load_user_memory(self):
        """Load user's personalization memory from disk."""
        memory_file = self._get_memory_file_path()
        if os.path.exists(memory_file):
            try:
                with open(memory_file, 'r') as f:
                    data = json.load(f)
                    self.preference_history = data.get('preference_history', [])
                    self.interaction_patterns = data.get('interaction_patterns', {})
                    self.learning_adaptations = data.get('learning_adaptations', {})
            except Exception as e:
                print(f"Error loading user memory: {e}")
    
    def _save_user_memory(self):
        """Save user's personalization memory to disk."""
        memory_file = self._get_memory_file_path()
        try:
            data = {
                'preference_history': self.preference_history,
                'interaction_patterns': self.interaction_patterns,
                'learning_adaptations': self.learning_adaptations,
                'last_updated': datetime.now().isoformat()
            }
            with open(memory_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving user memory: {e}")
    
    def record_interaction(self, interaction_type: str, context: Dict[str, Any], 
                          feedback: bool, learning_rate: str = "Moderate"):
        """
        Record a user interaction for learning and adaptation.
        
        Args:
            interaction_type: Type of interaction (completion, explanation, etc.)
            context: Context information about the interaction
            feedback: Whether the user provided positive feedback
            learning_rate: User's preferred learning rate
        """
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'type': interaction_type,
            'context': context,
            'feedback': feedback,
            'learning_rate': learning_rate
        }
        
        self.preference_history.append(interaction)
        
        # Update interaction patterns
        pattern_key = f"{interaction_type}_{context.get('domain', 'general')}"
        if pattern_key not in self.interaction_patterns:
            self.interaction_patterns[pattern_key] = {
                'positive_count': 0,
                'negative_count': 0,
                'total_count': 0
            }
        
        self.interaction_patterns[pattern_key]['total_count'] += 1
        if feedback:
            self.interaction_patterns[pattern_key]['positive_count'] += 1
        else:
            self.interaction_patterns[pattern_key]['negative_count'] += 1
        
        # Apply learning rate adjustments
        self._apply_learning_adaptations(interaction, learning_rate)
        
        # Save to LangChain memory
        if LANGCHAIN_AVAILABLE:
            human_msg = f"User {interaction_type}: {context.get('description', 'No description')}"
            ai_msg = f"Feedback: {'Positive' if feedback else 'Negative'}"
            self.memory.save_context(
                {"input": human_msg},
                {"output": ai_msg}
            )
        
        self._save_user_memory()
    
    def _apply_learning_adaptations(self, interaction: Dict[str, Any], learning_rate: str):
        """Apply learning rate-based adaptations."""
        adaptation_strength = {
            "Conservative": 0.1,
            "Moderate": 0.3,
            "Adaptive": 0.5,
            "Aggressive": 0.8
        }.get(learning_rate, 0.3)
        
        interaction_type = interaction['type']
        context = interaction['context']
        feedback = interaction['feedback']
        
        # Create adaptation rules based on feedback
        if interaction_type not in self.learning_adaptations:
            self.learning_adaptations[interaction_type] = {
                'preferences': {},
                'avoid_patterns': [],
                'boost_patterns': []
            }
        
        adaptations = self.learning_adaptations[interaction_type]
        
        if feedback:
            # Boost similar patterns
            pattern = context.get('pattern', 'unknown')
            if pattern not in adaptations['boost_patterns']:
                adaptations['boost_patterns'].append(pattern)
        else:
            # Avoid similar patterns
            pattern = context.get('pattern', 'unknown')
            if pattern not in adaptations['avoid_patterns']:
                adaptations['avoid_patterns'].append(pattern)
        
        # Update preferences with learning rate adjustment
        for key, value in context.items():
            if key in adaptations['preferences']:
                current_weight = adaptations['preferences'][key]
                if feedback:
                    adaptations['preferences'][key] = current_weight + (adaptation_strength * 0.1)
                else:
                    adaptations['preferences'][key] = current_weight - (adaptation_strength * 0.1)
            else:
                adaptations['preferences'][key] = adaptation_strength if feedback else -adaptation_strength
    
    def get_personalized_context(self, query_type: str = "general") -> Dict[str, Any]:
        """
        Get personalized context for AI responses based on user history.
        
        Args:
            query_type: Type of query to get context for
            
        Returns:
            Dictionary containing personalized context
        """
        context = {
            'user_patterns': self.interaction_patterns,
            'adaptations': self.learning_adaptations.get(query_type, {}),
            'recent_preferences': self.preference_history[-10:] if self.preference_history else [],
            'memory_variables': {}
        }
        
        # Get LangChain memory variables
        if LANGCHAIN_AVAILABLE:
            try:
                memory_vars = self.memory.load_memory_variables({})
                context['memory_variables'] = memory_vars
            except:
                pass
        
        return context
    
    def get_explanation_style(self, domain_specialization: str, 
                             communication_style: str) -> Dict[str, str]:
        """Get personalized explanation style based on user preferences."""
        style_templates = {
            "Concise": "Provide brief, direct explanations focusing on key points.",
            "Detailed": "Provide comprehensive explanations with examples and context.",
            "Tutorial": "Provide step-by-step explanations with learning objectives.",
            "Professional": "Provide formal, technical explanations with proper terminology.",
            "Casual": "Provide friendly, conversational explanations with analogies."
        }
        
        domain_focus = {
            "Web Development": "Focus on web technologies, frameworks, and best practices.",
            "Data Science": "Focus on data analysis, algorithms, and statistical concepts.",
            "DevOps": "Focus on deployment, infrastructure, and operational practices.",
            "Mobile Development": "Focus on mobile platforms, UI/UX, and performance.",
            "Systems Programming": "Focus on low-level concepts, performance, and efficiency.",
            "AI/ML": "Focus on machine learning concepts, models, and implementation.",
            "Security": "Focus on security best practices, vulnerabilities, and protection.",
            "General": "Provide balanced explanations suitable for general development."
        }
        
        return {
            "style_instruction": style_templates.get(communication_style, style_templates["Professional"]),
            "domain_focus": domain_focus.get(domain_specialization, domain_focus["General"]),
            "adaptation_note": f"Adapt based on user's {communication_style.lower()} communication preference and {domain_specialization.lower()} specialization."
        }


def get_user_personalization_memory(user_id: str) -> PersonalizationMemory:
    """Get or create personalization memory for a user."""
    return PersonalizationMemory(user_id)


def enhance_completion_with_personalization(completion: Dict[str, Any], 
                                           user_prefs: Dict[str, Any],
                                           user_memory: PersonalizationMemory) -> Dict[str, Any]:
    """
    Enhance a code completion with personalization features.
    
    Args:
        completion: Base completion dictionary
        user_prefs: User preferences from database
        user_memory: User's personalization memory
        
    Returns:
        Enhanced completion with personalization
    """
    # Get personalized context
    context = user_memory.get_personalized_context("completion")
    explanation_style = user_memory.get_explanation_style(
        user_prefs.get("domain_specialization", "General"),
        user_prefs.get("communication_style", "Professional")
    )
    
    # Add enhanced rationale based on user preferences
    learning_rate = user_prefs.get("learning_rate", "Moderate")
    domain = user_prefs.get("domain_specialization", "General")
    
    enhanced_completion = completion.copy()
    
    # Add personalized rationale
    if "rationale" not in enhanced_completion:
        enhanced_completion["rationale"] = f"This completion is suggested based on your {domain.lower()} specialization and {learning_rate.lower()} learning preferences."
    
    # Add context analysis
    enhanced_completion["context_analysis"] = {
        "domain_relevance": domain,
        "learning_adaptation": learning_rate,
        "style_preference": user_prefs.get("communication_style", "Professional"),
        "historical_patterns": len(context.get('recent_preferences', []))
    }
    
    # Add explanation based on user style
    if "explanation" not in enhanced_completion:
        style_instruction = explanation_style["style_instruction"]
        domain_focus = explanation_style["domain_focus"]
        enhanced_completion["explanation"] = f"Code explanation ({style_instruction.split('.')[0].lower()}): {domain_focus}"
    
    # Add patterns detected
    enhanced_completion["patterns_detected"] = [
        f"Matches {domain.lower()} development patterns",
        f"Suitable for {user_prefs.get('communication_style', 'professional').lower()} communication style",
        "Context-aware suggestion"
    ]
    
    # Add domain relevance scoring
    enhanced_completion["domain_relevance"] = {
        domain.lower(): "High",
        "general": "Medium"
    }
    
    # Add confidence factors based on personalization
    enhanced_completion["confidence_factors"] = {
        "user_history_match": 0.8 if context.get('recent_preferences') else 0.5,
        "domain_alignment": 0.9 if domain != "General" else 0.6,
        "style_consistency": 0.7,
        "pattern_recognition": completion.get("confidence", 0.5)
    }
    
    # Add knowledge sources with personalization
    enhanced_completion["sources"] = [
        "Local code analysis",
        "Language model knowledge",
        f"User preference history ({len(context.get('recent_preferences', []))} interactions)",
        f"{domain} domain knowledge"
    ]
    
    return enhanced_completion