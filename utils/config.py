"""Configuration and constants"""
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Get API key from secrets or environment
try:
    RAPIDAPI_KEY = st.secrets["RAPIDAPI_KEY"]
except:
    RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

# Page configuration
PAGE_CONFIG = {
    "page_title": "AI Resume Job Matcher",
    "page_icon": "🎯",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# API endpoints
JSEARCH_API_URL = "https://jsearch.p.rapidapi.com/search"
JSEARCH_API_HOST = "jsearch.p.rapidapi.com"

# Default values
DEFAULT_LOCATION = "Pune, India"
DEFAULT_JOB_TITLE = "Software Developer"
DEFAULT_SKILLS = ["Python", "JavaScript", "SQL"]