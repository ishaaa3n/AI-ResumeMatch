"""Main Streamlit application"""
import streamlit as st

# Import components
from components.header import render_header
from components.sidebar import render_sidebar
from components.profile_display import render_profile
from components.job_display import render_jobs, render_landing_page

# Import services
from services.pdf_parser import extract_text_from_pdf
from services.ai_analyzer import ResumeAnalyzer
from services.job_search import search_jobs

# Import utilities
from utils.config import PAGE_CONFIG, DEFAULT_LOCATION, DEFAULT_JOB_TITLE, DEFAULT_SKILLS, RAPIDAPI_KEY
from styles.custom_css import get_custom_css

# Page configuration
st.set_page_config(**PAGE_CONFIG)

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Check API key
if not RAPIDAPI_KEY:
    st.error("RapidAPI key not found. Please add RAPIDAPI_KEY=your_key to your .env file.")
    st.info("Get your free key at: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch")
    st.stop()

# Initialize AI analyzer
analyzer = ResumeAnalyzer()

# Render components
render_header()
render_sidebar()

# Main content
st.markdown("### 📤 Step 1: Upload Your Resume")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    uploaded_file = st.file_uploader(
        "Drop your PDF resume here",
        type=["pdf"],
        key="resume_uploader",
        help="Upload a text-based PDF (not scanned images)"
    )

if uploaded_file is not None:
    # Progress indicators
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Extract PDF text
        status_text.text("📄 Reading PDF...")
        progress_bar.progress(20)
        resume_text = extract_text_from_pdf(uploaded_file)
        progress_bar.progress(40)
        
        with st.expander("📄 View Extracted Text", expanded=False):
            st.text_area("Resume content", resume_text, height=200)
        
        # AI Analysis
        status_text.text("🤖 AI is analyzing your resume...")
        progress_bar.progress(60)
        
        try:
            parsed_info = analyzer.analyze_resume(resume_text)
            st.session_state["resume_info"] = parsed_info
            progress_bar.progress(100)
            status_text.text("✅ Analysis complete!")
            
            # Display profile
            render_profile(parsed_info)
            
        except Exception as e:
            st.warning(f"⚠️ AI parsing issue. Using fallback...")
            st.session_state["resume_info"] = {
                "full_name": "Not extracted",
                "job_title": DEFAULT_JOB_TITLE,
                "years_experience": 0,
                "top_skills": DEFAULT_SKILLS,
                "preferred_location": DEFAULT_LOCATION
            }
        
        # Job Search Section
        st.markdown("---")
        st.markdown("### 🔍 Step 2: Search for Jobs")
        
        # Get resume info
        info = st.session_state.get("resume_info", {})
        job_title = (info.get("job_title") or "").strip()
        default_location = (info.get("preferred_location") or DEFAULT_LOCATION).strip()
        top_skills = info.get("top_skills") or []
        
        # Default keywords
        if job_title and job_title.lower() not in ["not found", "not extracted", ""]:
            default_keywords = job_title
        elif top_skills:
            default_keywords = top_skills[0]
        else:
            default_keywords = DEFAULT_JOB_TITLE
        
        # Search form
        with st.form("job_search_form"):
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                search_keywords = st.text_input("🔎 Job Keywords", value=default_keywords)
            
            with col2:
                search_location = st.text_input("📍 Location", value=default_location)
            
            with col3:
                date_filter = st.selectbox(
                    "📅 Posted",
                    ["month", "week", "3days", "today", "all"],
                    format_func=lambda x: {"all": "All time", "today": "Today", "3days": "3 days", "week": "Week", "month": "Month"}[x]
                )
            
            search_button = st.form_submit_button("🚀 Search Jobs", use_container_width=True)
        
        # Execute search
        if search_button:
            with st.spinner("🔍 Searching across Google Jobs, LinkedIn, Indeed..."):
                try:
                    jobs = search_jobs(search_keywords, search_location, date_filter)
                    render_jobs(jobs, search_keywords, search_location)
                except Exception as e:
                    st.error(f"❌ Search error: {str(e)}")
    
    except ValueError as e:
        st.error(f"❌ {str(e)}")
        st.info("💡 Try a text-based PDF (not a scanned image)")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        with st.expander("🐛 Debug Info"):
            import traceback
            st.code(traceback.format_exc())

else:
    # Landing page
    render_landing_page()