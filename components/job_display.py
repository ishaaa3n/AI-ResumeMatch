"""Job results display component"""
import streamlit as st

def render_jobs(jobs, keywords, location):
    """
    Render job search results
    
    Args:
        jobs (list): List of job dictionaries
        keywords (str): Search keywords used
        location (str): Location used for search
    """
    st.markdown("---")
    st.markdown(f"### 💼 Jobs for **{keywords}** in **{location}**")
    
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
        st.info("💡 **Try:**\n- Broader keywords\n- Different location\n- 'All time' date filter")

def render_landing_page():
    """Render the landing page when no file is uploaded"""
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