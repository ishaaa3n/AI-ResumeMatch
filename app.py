"""Main Streamlit application - AI Resume Job Matcher"""
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

def _generate_search_strategies(info):
    """
    Generate multiple search strategies based on resume info
    
    Args:
        info (dict): Resume information
        
    Returns:
        list: List of search strategy dictionaries
    """
    strategies = []
    
    job_title = (info.get("job_title") or "").strip()
    top_skills = info.get("top_skills") or []
    location = (info.get("preferred_location") or "Pune, India").strip()
    years_exp = info.get("years_experience", 0)
    
    # Strategy 1: Primary job title
    if job_title and job_title.lower() not in ["not found", "not extracted", ""]:
        strategies.append({
            "keywords": job_title,
            "location": location
        })
    
    # Strategy 2: Top skill + "developer/engineer/intern"
    if top_skills:
        main_skill = top_skills[0]
        if years_exp == 0:
            strategies.append({
                "keywords": f"{main_skill} intern",
                "location": location
            })
            strategies.append({
                "keywords": f"{main_skill} entry level",
                "location": location
            })
        else:
            strategies.append({
                "keywords": f"{main_skill} developer",
                "location": location
            })
    
    # Strategy 3: Combination of top skills
    if len(top_skills) >= 2:
        skill_combo = f"{top_skills[0]} {top_skills[1]}"
        strategies.append({
            "keywords": skill_combo,
            "location": location
        })
    
    # Strategy 4: Broader location search if specific location yields few results
    if "," in location:  # e.g., "Pune, India"
        country = location.split(",")[-1].strip()
        if job_title and job_title.lower() not in ["not found", "not extracted", ""]:
            strategies.append({
                "keywords": job_title,
                "location": country
            })
    
    # Ensure at least one strategy
    if not strategies:
        strategies.append({
            "keywords": "entry level developer" if years_exp == 0 else "developer",
            "location": location
        })
    
    return strategies[:4]  # Limit to 4 strategies to avoid too many API calls

def _perform_auto_search(info):
    """Perform automatic job search based on AI analysis"""
    # Generate search strategies
    strategies = _generate_search_strategies(info)
    
    all_jobs = []
    seen_links = set()  # Avoid duplicates
    
    with st.spinner("🔍 AI is searching multiple job sources..."):
        progress_bar = st.progress(0)
        
        for idx, strategy in enumerate(strategies):
            st.caption(f"🔎 Searching: {strategy['keywords']} in {strategy['location']}")
            
            try:
                jobs = search_jobs(
                    strategy['keywords'],
                    strategy['location'],
                    "month",
                    num_results=5,
                    resume_info=info
                )
                
                # Add unique jobs
                for job in jobs:
                    if job['link'] not in seen_links:
                        seen_links.add(job['link'])
                        all_jobs.append(job)
                
            except Exception as e:
                st.warning(f"⚠️ Search '{strategy['keywords']}' failed: {str(e)}")
            
            progress_bar.progress((idx + 1) / len(strategies))
        
        progress_bar.empty()
    
    if all_jobs:
        # Sort by relevance (you can add scoring logic here)
        render_jobs(all_jobs[:10], "AI-matched positions", info.get('preferred_location', 'Multiple locations'))
    else:
        st.warning("😔 No jobs found. Try customizing the search.")
        st.info("💡 Click 'Customize Search' below to try different keywords or locations.")

def _perform_custom_search(keywords, location, date_filter, info):
    """Perform custom search with user overrides"""
    # Use AI values if custom values not provided
    if not keywords:
        job_title = (info.get("job_title") or "").strip()
        top_skills = info.get("top_skills") or []
        
        if job_title and job_title.lower() not in ["not found", "not extracted", ""]:
            keywords = job_title
        elif top_skills:
            keywords = top_skills[0]
        else:
            keywords = "Software Developer"
    
    if not location:
        location = (info.get("preferred_location") or "Pune, India").strip()
    
    with st.spinner("🔍 Searching with your custom settings..."):
        try:
            jobs = search_jobs(
                keywords,
                location,
                date_filter,
                num_results=10,
                resume_info=info
            )
            render_jobs(jobs, keywords, location)
        except Exception as e:
            st.error(f"❌ Search error: {str(e)}")

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
        
        # === Automatic Job Search ===
        st.markdown("---")
        st.markdown("### 🔍 Step 2: AI-Matched Job Recommendations")
        
        # Get resume info
        info = st.session_state.get("resume_info", {})
        
        # Show what AI will search for
        st.info("🤖 **AI will automatically find the best job matches for your profile**")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**🎯 Search Strategy:**")
            st.write(f"• **Primary:** {info.get('job_title', 'Software Developer')}")
            top_skills_display = ', '.join(info.get('top_skills', [])[:3])
            st.write(f"• **Skills:** {top_skills_display if top_skills_display else 'General'}")
            st.write(f"• **Location:** {info.get('preferred_location', 'Pune, India')}")
        
        with col2:
            years_exp = info.get('years_experience', 0)
            if years_exp == 0:
                st.markdown("**🎓 Experience Level:** Fresher/Student")
                st.caption("Looking for: Internships, Entry-level, Trainee roles")
            elif years_exp <= 2:
                st.markdown("**💼 Experience Level:** Junior")
                st.caption("Looking for: Junior, Associate roles")
            elif years_exp <= 5:
                st.markdown("**📈 Experience Level:** Mid-level")
                st.caption("Looking for: Mid-level positions")
            else:
                st.markdown("**⭐ Experience Level:** Senior")
                st.caption("Looking for: Senior, Lead positions")
        
        # Advanced search options (collapsible)
        with st.expander("🎛️ Customize Search (Optional)", expanded=False):
            st.caption("💡 Only use this if you want to override AI recommendations")
            
            with st.form("custom_search_form"):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    custom_keywords = st.text_input(
                        "Custom Keywords",
                        value="",
                        placeholder="Leave empty to use AI recommendations"
                    )
                
                with col2:
                    custom_location = st.text_input(
                        "Custom Location",
                        value="",
                        placeholder="Leave empty to use AI recommendations"
                    )
                
                with col3:
                    date_filter = st.selectbox(
                        "Posted",
                        ["month", "week", "3days", "today", "all"],
                        format_func=lambda x: {
                            "all": "All time",
                            "today": "Today",
                            "3days": "3 days",
                            "week": "Week",
                            "month": "Month"
                        }[x]
                    )
                
                custom_search_button = st.form_submit_button("🔍 Search with Custom Settings", use_container_width=True)
            
            # Handle custom search
            if custom_search_button:
                _perform_custom_search(custom_keywords, custom_location, date_filter, info)
        
        # Auto-search button (primary action)
        st.markdown("")  # Spacing
        if st.button("🚀 Find Jobs Automatically", type="primary", use_container_width=True):
            _perform_auto_search(info)
    
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