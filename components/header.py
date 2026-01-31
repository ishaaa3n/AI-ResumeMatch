"""Header component"""
import streamlit as st

def render_header():
    """Render the main header"""
    st.markdown('<h1 class="main-title">🎯 AI Resume Job Matcher</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Upload your resume • AI extracts skills • Find matching jobs instantly</p>', unsafe_allow_html=True)