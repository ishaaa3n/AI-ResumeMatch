"""Sidebar component"""
import streamlit as st
import requests
from utils.config import RAPIDAPI_KEY, JSEARCH_API_URL, JSEARCH_API_HOST

def render_sidebar():
    """Render the sidebar with API test and info"""
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/000000/resume.png", width=80)
        st.markdown("### 🛠️ Configuration")
        
        # API Test
        with st.expander("🔌 Test API Connection", expanded=False):
            if st.button("Test RapidAPI", use_container_width=True):
                _test_api_connection()
        
        # Show API key status
        if RAPIDAPI_KEY:
            masked_key = RAPIDAPI_KEY[:6] + "•••" + RAPIDAPI_KEY[-4:]
            st.caption(f"🔑 API Key: `{masked_key}`")
        
        st.markdown("---")
        
        # How it works
        st.markdown("### 📖 How it works")
        st.markdown("""
        1️⃣ **Upload** your resume (PDF)
        
        2️⃣ **AI analyzes** your skills & experience
        
        3️⃣ **Search** for matching jobs
        
        4️⃣ **Apply** directly to positions
        """)
        
        st.markdown("---")
        st.caption("Powered by:")
        st.caption("🤖 Ollama (Llama3)")
        st.caption("🔍 RapidAPI JSearch")
        st.caption("⚡ Streamlit")

def _test_api_connection():
    """Test RapidAPI connection"""
    with st.spinner("Testing..."):
        test_headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": JSEARCH_API_HOST
        }
        test_params = {
            "query": "Python Developer in USA",
            "page": "1",
            "num_pages": "1"
        }
        
        try:
            response = requests.get(JSEARCH_API_URL, headers=test_headers, params=test_params, timeout=10)
            
            if response.status_code == 200:
                st.success("✅ Connected!")
                data = response.json()
                st.info(f"Found {len(data.get('data', []))} test jobs")
            elif response.status_code == 403:
                st.error("❌ Not subscribed")
                st.caption("[Subscribe here](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch)")
            elif response.status_code == 429:
                st.warning("⚠️ Rate limit hit")
            else:
                st.error(f"Error: {response.status_code}")
        except Exception as e:
            st.error(f"Failed: {str(e)}")