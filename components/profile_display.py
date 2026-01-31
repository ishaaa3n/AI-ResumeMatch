"""Profile display component"""
import streamlit as st

def render_profile(parsed_info):
    """
    Render the extracted profile information
    
    Args:
        parsed_info (dict): Parsed resume information
    """
    # st.markdown("### 👤 Your Profile")
    
    # # Profile cards
    # col1, col2, col3, col4 = st.columns(4)
    
    # with col1:
    #     st.markdown(f"""
    #     <div class="stat-card">
    #         <div class="stat-value">👨‍💼</div>
    #         <div class="stat-label">Name</div>
    #         <div style="font-weight: 600; margin-top: 0.5rem;">{parsed_info.get("full_name", "N/A")}</div>
    #     </div>
    #     """, unsafe_allow_html=True)
    
    # with col2:
    #     st.markdown(f"""
    #     <div class="stat-card">
    #         <div class="stat-value">💼</div>
    #         <div class="stat-label">Role</div>
    #         <div style="font-weight: 600; margin-top: 0.5rem;">{parsed_info.get("job_title", "N/A")}</div>
    #     </div>
    #     """, unsafe_allow_html=True)
    
    # with col3:
    #     st.markdown(f"""
    #     <div class="stat-card">
    #         <div class="stat-value">{parsed_info.get('years_experience', 0)}</div>
    #         <div class="stat-label">Years Experience</div>
    #     </div>
    #     """, unsafe_allow_html=True)
    
    # with col4:
    #     st.markdown(f"""
    #     <div class="stat-card">
    #         <div class="stat-value">📍</div>
    #         <div class="stat-label">Location</div>
    #         <div style="font-weight: 600; margin-top: 0.5rem;">{parsed_info.get("preferred_location", "Pune")}</div>
    #     </div>
    #     """, unsafe_allow_html=True)
    
    # Skills section
    st.markdown("#### 🎯 Your Top Skills")
    skills = parsed_info.get("top_skills", [])
    skills_html = "".join([f'<span class="skill-badge">{skill}</span>' for skill in skills[:10]])
    st.markdown(f'<div style="margin: 1rem 0;">{skills_html}</div>', unsafe_allow_html=True)