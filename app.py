import streamlit as st
import os
from dotenv import load_dotenv
import requests
from PyPDF2 import PdfReader
from langchain_community.llms import Ollama
import json

load_dotenv()

# API Keys
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

if not RAPIDAPI_KEY:
    st.error("RapidAPI key not found. Please add RAPIDAPI_KEY=your_key to your .env file.")
    st.info("Get your free key at: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch")
    st.stop()

# Initialize Ollama
llm = Ollama(model="llama3", temperature=0.3)

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="AI Resume Job Matcher",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== CUSTOM CSS =====
st.markdown("""
<style>
    /* Main title styling */
    .main-title {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    /* Subtitle styling */
    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Card styling */
    .info-card {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    /* Stats card */
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        text-align: center;
        border-top: 3px solid #667eea;
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
    
    .stat-label {
        color: #6b7280;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Job card styling */
    .job-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        border-left: 4px solid #10b981;
        transition: transform 0.2s;
    }
    
    .job-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
    }
    
    /* Profile section */
    .profile-section {
        background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
        padding: 2rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    /* Badge styling */
    .skill-badge {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 0.2rem;
        font-weight: 500;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* Remove extra padding */
    .block-container {
        padding-top: 2rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea15 0%, #764ba215 100%);
    }
</style>
""", unsafe_allow_html=True)

# ===== HEADER =====
st.markdown('<h1 class="main-title">🎯 AI Resume Job Matcher</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Upload your resume • AI extracts skills • Find matching jobs instantly</p>', unsafe_allow_html=True)

# ===== SIDEBAR =====
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/resume.png", width=80)
    st.markdown("### 🛠️ Configuration")
    
    # API Test
    with st.expander("🔌 Test API Connection", expanded=False):
        if st.button("Test RapidAPI", use_container_width=True):
            with st.spinner("Testing..."):
                test_url = "https://jsearch.p.rapidapi.com/search"
                test_headers = {
                    "X-RapidAPI-Key": RAPIDAPI_KEY,
                    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
                }
                test_params = {
                    "query": "Python Developer in USA",
                    "page": "1",
                    "num_pages": "1"
                }
                
                try:
                    response = requests.get(test_url, headers=test_headers, params=test_params, timeout=10)
                    
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

# ===== MAIN CONTENT =====

# File Upload Section
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
    
    # Progress indicator
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # === Extract text from PDF ===
        status_text.text("📄 Reading PDF...")
        progress_bar.progress(20)
        
        pdf_reader = PdfReader(uploaded_file)
        resume_text = ""
        
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                resume_text += page_text

        resume_text = resume_text.strip()
        if not resume_text:
            st.error("❌ No text could be extracted from the PDF.")
            st.info("💡 Try a text-based PDF (not a scanned image)")
            st.stop()

        progress_bar.progress(40)
        
        with st.expander("📄 View Extracted Text", expanded=False):
            st.text_area("Resume content", resume_text, height=200)

        # === AI Analysis ===
        status_text.text("🤖 AI is analyzing your resume...")
        progress_bar.progress(60)

        extraction_prompt = """You are a resume parser. Extract info from this resume and return ONLY a JSON object (no markdown, no explanations).

Resume text:
{resume_text}

Return this exact JSON structure:
{{"full_name": "name here", "job_title": "title here", "years_experience": 3, "top_skills": ["skill1", "skill2", "skill3"], "preferred_location": "Pune"}}

JSON only:"""

        resume_snippet = resume_text[:1500] if len(resume_text) > 1500 else resume_text

        try:
            raw_response = llm.invoke(
                extraction_prompt.format(resume_text=resume_snippet)
            )

            # Clean response
            cleaned = (raw_response or "").strip()
            
            if not cleaned:
                raise ValueError("Empty response from AI")

            if "```json" in cleaned:
                cleaned = cleaned.split("```json")[1].split("```")[0].strip()
            elif "```" in cleaned:
                cleaned = cleaned.split("```")[1].split("```")[0].strip()

            if "{" in cleaned:
                cleaned = cleaned[cleaned.index("{"):]

            if "}" in cleaned:
                cleaned = cleaned[:cleaned.rindex("}") + 1]

            parsed_info = json.loads(cleaned)
            st.session_state["resume_info"] = parsed_info
            
            progress_bar.progress(100)
            status_text.text("✅ Analysis complete!")

            # === Display Profile ===
            st.markdown("### 👤 Your Profile")
            
            # Profile cards
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">👨‍💼</div>
                    <div class="stat-label">Name</div>
                    <div style="font-weight: 600; margin-top: 0.5rem;">{parsed_info.get("full_name", "N/A")}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">💼</div>
                    <div class="stat-label">Role</div>
                    <div style="font-weight: 600; margin-top: 0.5rem;">{parsed_info.get("job_title", "N/A")}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{parsed_info.get('years_experience', 0)}</div>
                    <div class="stat-label">Years Experience</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">📍</div>
                    <div class="stat-label">Location</div>
                    <div style="font-weight: 600; margin-top: 0.5rem;">{parsed_info.get("preferred_location", "Pune")}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Skills section
            st.markdown("#### 🎯 Top Skills")
            skills = parsed_info.get("top_skills", [])
            skills_html = "".join([f'<span class="skill-badge">{skill}</span>' for skill in skills[:10]])
            st.markdown(f'<div style="margin: 1rem 0;">{skills_html}</div>', unsafe_allow_html=True)

        except (json.JSONDecodeError, ValueError) as e:
            st.warning(f"⚠️ AI parsing issue. Using fallback...")
            
            st.session_state["resume_info"] = {
                "full_name": "Not extracted",
                "job_title": "Software Developer",
                "years_experience": 0,
                "top_skills": ["Python", "JavaScript", "SQL"],
                "preferred_location": "Pune"
            }

        except Exception as e:
            st.error(f"❌ AI analysis error: {str(e)}")
            st.session_state["resume_info"] = {
                "full_name": "Not extracted",
                "job_title": "Software Developer",
                "years_experience": 0,
                "top_skills": ["Python"],
                "preferred_location": "Pune"
            }

        # === Job Search Section ===
        st.markdown("---")
        st.markdown("### 🔍 Step 2: Search for Jobs")

        # Get resume info safely
        info = st.session_state.get("resume_info", {})
        job_title = (info.get("job_title") or "").strip()
        default_location = (info.get("preferred_location") or "Pune, India").strip()
        top_skills = info.get("top_skills") or []
        
        # Create default keywords
        if job_title and job_title.lower() not in ["not found", "not extracted", ""]:
            default_keywords = job_title
        elif top_skills and len(top_skills) > 0:
            default_keywords = top_skills[0]
        else:
            default_keywords = "Software Developer"

        # Search form
        with st.form("job_search_form"):
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                search_keywords = st.text_input(
                    "🔎 Job Keywords",
                    value=default_keywords,
                    placeholder="e.g., Python Developer, Data Analyst"
                )
            
            with col2:
                search_location = st.text_input(
                    "📍 Location",
                    value=default_location,
                    placeholder="e.g., Pune, India"
                )
            
            with col3:
                date_filter = st.selectbox(
                    "📅 Posted",
                    ["month", "week", "3days", "today", "all"],
                    format_func=lambda x: {
                        "all": "All time",
                        "today": "Today",
                        "3days": "3 days",
                        "week": "Week",
                        "month": "Month"
                    }[x]
                )
            
            search_button = st.form_submit_button("🚀 Search Jobs", use_container_width=True)

        # === Job Search Function ===
        def search_jobs_rapidapi(keywords, location, date_posted="month", num_results=10):
            url = "https://jsearch.p.rapidapi.com/search"
            
            headers = {
                "X-RapidAPI-Key": RAPIDAPI_KEY,
                "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
            }
            
            keywords = (keywords or "developer").strip()
            location = (location or "India").strip()
            query = f"{keywords} in {location}"
            
            querystring = {
                "query": query,
                "page": "1",
                "num_pages": "1",
                "date_posted": date_posted
            }
            
            try:
                response = requests.get(url, headers=headers, params=querystring, timeout=15)
                response.raise_for_status()
                data = response.json()
                
                jobs = []
                for job in data.get("data", [])[:num_results]:
                    title = job.get("job_title") or "N/A"
                    company = job.get("employer_name") or "N/A"
                    city = job.get("job_city") or ""
                    country = job.get("job_country") or ""
                    location_str = f"{city}, {country}".strip(", ") or "N/A"
                    description = (job.get("job_description") or "No description available")[:500] + "..."
                    link = job.get("job_apply_link") or "#"
                    posted = (job.get("job_posted_at_datetime_utc") or "N/A")[:10]
                    employment_type = job.get("job_employment_type") or "N/A"
                    source = job.get("job_publisher") or "N/A"
                    
                    salary = ""
                    if job.get("job_min_salary") and job.get("job_max_salary"):
                        currency = job.get("job_salary_currency") or ""
                        min_sal = job.get("job_min_salary") or ""
                        max_sal = job.get("job_max_salary") or ""
                        salary = f"{currency} {min_sal:,} - {max_sal:,}"
                    
                    jobs.append({
                        "title": title,
                        "company": company,
                        "location": location_str,
                        "description": description,
                        "link": link,
                        "posted": posted,
                        "salary": salary,
                        "employment_type": employment_type,
                        "source": source
                    })
                
                return jobs
                
            except requests.exceptions.HTTPError as he:
                st.error(f"❌ HTTP Error: {he}")
                if response.status_code == 403:
                    st.error("Invalid API key. Please check your subscription.")
                elif response.status_code == 429:
                    st.error("Rate limit exceeded (150/month).")
                return []
            except Exception as e:
                st.error(f"❌ Search error: {str(e)}")
                return []

        # === Display Jobs ===
        if search_button:
            st.markdown("---")
            st.markdown(f"### 💼 Jobs for **{search_keywords}** in **{search_location}**")
            
            with st.spinner("🔍 Searching across Google Jobs, LinkedIn, Indeed..."):
                jobs = search_jobs_rapidapi(search_keywords, search_location, date_filter)

            if jobs:
                st.success(f"✨ Found **{len(jobs)}** matching positions!")
                
                for idx, job in enumerate(jobs, 1):
                    with st.expander(f"**{job['title']}** at {job['company']}", expanded=(idx <= 2)):
                        
                        col_left, col_right = st.columns([3, 1])
                        
                        with col_left:
                            st.markdown(f"**🏢 Company:** {job['company']}")
                            st.markdown(f"**📍 Location:** {job['location']}")
                            st.markdown(f"**💼 Type:** {job['employment_type']}")
                            if job['salary']:
                                st.markdown(f"**💰 Salary:** {job['salary']}")
                            st.markdown(f"**📅 Posted:** {job['posted']}")
                            st.markdown(f"**🌐 Via:** {job['source']}")
                        
                        with col_right:
                            st.markdown(f"[![Apply Now](https://img.shields.io/badge/Apply-Now-success?style=for-the-badge)]({job['link']})")
                        
                        st.markdown("**📝 Description:**")
                        st.write(job['description'])
                
            else:
                st.warning("😔 No jobs found matching your criteria.")
                st.info("💡 **Try:**\n- Broader keywords (e.g., 'Developer' instead of 'Senior React Developer')\n- Different location\n- 'All time' date filter")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        with st.expander("🐛 Debug Info"):
            import traceback
            st.code(traceback.format_exc())

else:
    # Landing state
    st.markdown("""
    <div class="info-card">
        <h3>✨ Get Started</h3>
        <p>Upload your resume above to discover jobs matching your skills and experience.</p>
        <ul>
            <li>📄 Supports PDF format</li>
            <li>🤖 AI-powered skill extraction</li>
            <li>🌐 Real-time job search across major platforms</li>
            <li>⚡ Instant results</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Demo stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🎯 Resumes Analyzed", "1000+")
    with col2:
        st.metric("💼 Jobs Available", "50K+")
    with col3:
        st.metric("⚡ Avg. Search Time", "< 10s")