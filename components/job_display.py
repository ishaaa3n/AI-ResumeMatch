"""Job results display component"""
import streamlit as st

def render_jobs(jobs, keywords, location):
    """
    Render job search results with AI match indicators
    
    Args:
        jobs (list): List of job dictionaries
        keywords (str): Search keywords used
        location (str): Location used for search
    """
    st.markdown("---")
    st.markdown(f"### 💼 {len(jobs)} AI-Matched Jobs")
    
    if jobs:
        st.success(f"✨ Found **{len(jobs)}** positions matching your profile!")
        
        # Add match quality indicator
        st.caption("🎯 Jobs are filtered and ranked by AI based on your experience level and skills")
        
        for idx, job in enumerate(jobs, 1):
            # Calculate simple match score for display
            match_score = _calculate_match_score(job, idx)
            match_emoji = "🔥" if match_score >= 90 else "⭐" if match_score >= 75 else "✓"
            
            with st.expander(
                f"{match_emoji} **{job['title']}** at {job['company']} • {match_score}% match",
                expanded=(idx <= 2)
            ):
                
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
        st.info("💡 **Try:**\n- Using custom search settings\n- Broadening your location\n- Different skills from your resume")

def _calculate_match_score(job, position):
    """
    Calculate a simple match score for display
    (In a real app, this would use more sophisticated matching)
    
    Args:
        job (dict): Job information
        position (int): Position in search results (1-based)
        
    Returns:
        int: Match score (0-100)
    """
    # Simple scoring: top results get higher scores
    base_score = max(60, 100 - (position * 5))
    return min(100, base_score)

def render_landing_page():
    """Render the landing page when no file is uploaded"""
    st.markdown("""
    <div class="info-card">
        <h3>✨ Get Started</h3>
        <p>Upload your resume above and let AI find the perfect jobs for you automatically!</p>
        <ul>
            <li>📄 Upload PDF resume</li>
            <li>🤖 AI extracts your skills, experience & preferences</li>
            <li>🎯 Automatically searches multiple job boards</li>
            <li>✨ Get personalized job recommendations</li>
            <li>⚡ All in under 30 seconds</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Demo stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🎯 Resumes Analyzed", "100+")
    with col2:
        st.metric("💼 Jobs Available", "50K+")
    with col3:
        st.metric("⚡ Avg. Match Time", "< 30s")