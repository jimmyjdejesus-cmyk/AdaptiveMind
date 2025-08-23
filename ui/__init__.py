"""
UI components for Jarvis AI
"""

import sys
from pathlib import Path

# Add legacy path for imports
legacy_path = Path(__file__).parent.parent / "legacy"
sys.path.insert(0, str(legacy_path))

try:
    from ui.sidebar import sidebar
    from ui.analytics import render_analytics_dashboard
    from ui.cerebro import create_cerebro_app, CerebroDashboard
except ImportError:
    # Fallback implementations
    import streamlit as st
    
    def sidebar():
        """Fallback sidebar implementation"""
        st.sidebar.title("🤖 Jarvis AI")
        st.sidebar.info("Legacy UI not available")
        return None
    
    def render_analytics_dashboard():
        """Fallback analytics dashboard"""
        st.subheader("📊 Analytics Dashboard")
        st.info("Analytics features not available - check legacy implementation")

    def create_cerebro_app(*args, **kwargs):
        """Fallback Cerebro app constructor."""
        raise ImportError("Cerebro dashboard not available")

    class CerebroDashboard:  # type: ignore
        """Placeholder dashboard when Cerebro is unavailable."""
        pass
