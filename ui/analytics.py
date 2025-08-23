"""Placeholder analytics dashboard for the Jarvis AI UI.

Provides basic metrics and a sample chart when real analytics data are
unavailable. This keeps the analytics page functional until backend
integration is completed.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st


def render_analytics_dashboard() -> None:
    """Render a minimal analytics dashboard."""
    st.subheader("\ud83d\udcca Analytics Dashboard")
    st.info(
        "Advanced analytics are not yet connected. Displaying sample data "
        "for demonstration purposes."
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Conversations", "0")
    with col2:
        st.metric("Messages", "0")
    with col3:
        st.metric("Active Users", "0")

    chart_data = pd.DataFrame({"Day": range(1, 8), "Conversations": [0] * 7})
    st.line_chart(chart_data.set_index("Day"))


__all__ = ["render_analytics_dashboard"]
