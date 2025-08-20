# Jarvis AI

## Repository Structure

This repository is organized as follows:

### Legacy Code
All previous implementation of the Jarvis AI assistant has been archived in the `legacy/` folder. This includes:
- Original Python application files
- Database implementation
- UI components
- Agent implementation
- Authentication system
- Tools and plugins
- Documentation

## New Development
The root directory now serves as the starting point for the next phase of development. Future implementations will be built here while preserving the legacy code for reference.

## Getting Started

## Quick Demo Script
.\venv\Scripts\python.exe -m streamlit run ui_demo.py

To work with this repository:

1. **Legacy Code**: Explore the `legacy/` folder for the previous implementation
2. **New Development**: Build new features in the root directory

## Completed Features 

## Coding Tools
Code explanation generation: Added context-aware explanations for code completions that adapt to user's communication style and domain specialization
Completion rationale display: Implemented detailed reasoning display showing confidence factors, pattern recognition, and decision logic behind AI suggestions
Knowledge source attribution: Added comprehensive source tracking including user interaction history, domain knowledge, and model confidence factors

Learning rate adjustment: Implemented 4-tier learning system (Conservative, Moderate, Adaptive, Aggressive) controlling how quickly AI adapts to user preferences
Domain specialization settings: Added 8 specialized domains (Web Development, Data Science, DevOps, etc.) with tailored response patterns
Style preference configuration: Implemented 5 communication styles (Concise, Detailed, Tutorial, Professional, Casual) affecting all AI interactions

The implementation follows the documented Lang ecosystem approach:
LangChain Memory: Created PersonalizationMemory class for persistent user learning and adaptation
LangGraph workflows: Enhanced existing workflow with personalization initialization, explanation generation, and feedback processing nodes
LangGraphUI visualization: Added interactive personalized workflow views with user context panels and quick feedback collection
Enhanced Code Intelligence: Integrated personalization engine that generates contextually relevant suggestions

#UI Enhancements
learning_rate = st.selectbox("AI Learning Rate", ["Conservative", "Moderate", "Adaptive", "Aggressive"])
domain = st.selectbox("Domain Specialization", ["General", "Web Development", "Data Science", ...])
style = st.selectbox("Communication Style", ["Concise", "Detailed", "Tutorial", ...])

## Contact

For questions or support, please contact the repository owner.
