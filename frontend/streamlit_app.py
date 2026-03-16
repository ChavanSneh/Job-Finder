import streamlit as st
import requests

# Configure page
st.set_page_config(page_title="Job Scout 2026", layout="wide")
st.title("⚔️ Job Scout: Command Center")

# Sidebar
with st.sidebar:
    st.header("👤 Your Profile")
    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    st.divider()
    exp = st.number_input("Experience (Years)", 0, 50, 2)
    skills = st.text_area("Skill Arsenal", placeholder="Python, FastAPI, AI, etc...")

# Main Search Area
col_a, col_b = st.columns(2)
with col_a:
    target = st.text_input("Target Job", placeholder="e.g. AI Engineer")
with col_b:
    location = st.text_input("Location", "Pune")

if st.button("🚀 DEPLOY", type="primary"):
    if not target:
        st.warning("Please enter a Target Job title.")
        st.stop()

    form_data = {
        "title": target,
        "location": location,
        "exp": exp,
        "skills": skills
    }
    
    # Correctly package the file
    files = None
    if resume_file:
        files = {"resume": (resume_file.name, resume_file.getvalue(), "application/pdf")}

    try:
        with st.spinner("Analyzing market data with Gemini..."):
            # FIXED: Point to localhost, not the 'backend' hostname
            response = requests.post(
                "http://127.0.0.1:8000/search_jobs", 
                data=form_data, 
                files=files,
                timeout=60  # Added timeout to prevent hanging
            )
        
        if response.status_code == 200:
            data = response.json()
            
            # AI Insight
            insight = data.get("ai_insight", "No analysis available.")
            st.info(f"### 🧠 Gemini Intelligence\n{insight}")
            
            # Job Display
            jobs = data.get("jobs", [])
            if not jobs:
                st.warning("No specific roles found. Try adjusting your target.")
            
            for i, job in enumerate(jobs):
                with st.container(border=True):
                    st.subheader(job.get('title', 'Unknown Title'))
                    st.write(f"🏢 **Company:** {job.get('company', 'N/A')}")
                    
                    # Wrap buttons in a layout
                    cols = st.columns([1, 1, 4])
                    with cols[0]:
                        st.link_button("🔗 Apply", job.get('link', '#'))
                    with cols[1]:
                        if st.button("⏭️ Skip", key=f"skip_{i}"):
                            st.toast(f"Skipped {job.get('title')}")

        else:
            st.error(f"Mission Failed: Backend returned status {response.status_code}")
            st.code(response.text)
            
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to backend. Is `uvicorn` running at 127.0.0.1:8000?")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")