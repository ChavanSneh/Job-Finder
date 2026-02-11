import streamlit as st
import asyncio
from google import genai
import os
from playwright.async_api import async_playwright
import time
import pandas as pd  # Added for the 'Save' feature

# ==========================================
# 🛡️ 1. ENHANCED SCOUTING ENGINE
# ==========================================
async def auto_scout(job_title, stealth, limit):
    findings = []
    async with async_playwright() as p:
        # Launch with a realistic window size
        browser = await p.chromium.launch(headless=not stealth)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        # Scouting URL
        search_url = f"https://www.google.com/search?q={job_title}+jobs+in+Pune"
        await page.goto(search_url, wait_until="domcontentloaded")
        
        # Wait a moment for dynamic results to pop in
        await page.wait_for_timeout(2000)
        
        # More robust selectors to find job titles/links
        selectors = ["h3", ".DKV0Md", ".j7vP8b", "div[role='heading']"]
        combined_selector = ", ".join(selectors)
        
        links = await page.locator(combined_selector).all()
        
        for link in links:
            if len(findings) >= limit:
                break
            text = await link.inner_text()
            if text and len(text) > 5:
                findings.append(text.strip())
                
        await browser.close()
    return findings if findings else ["No leads found. Try a broader search term."]

# ==========================================
# 🧠 2. AI INTELLIGENCE (Gemini 1.5 Flash)
# ==========================================
client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

def ai_analyze(job_title, findings, intel):
    if not client: return "❌ API Key Missing."
    
    prompt = f"""
    MISSION: Professional Job Analysis
    Target Role: {job_title} in Pune
    Warrior Stats: {intel['exp']} yrs exp, Skills: {intel['skills']}
    
    Leads Found: {findings}
    
    MISSION OBJECTIVES:
    1. MATCHING: Evaluate these leads against the Warrior's skills.
    2. SCORING: Give a Match % for the top leads.
    3. STRATEGY: Draft a 2-line intro email from {intel['email']}.
    Format the output with bold headers and bullet points.
    """
    
    for attempt in range(2):
        try:
            response = client.models.generate_content(
                model="models/gemini-1.5-flash", 
                contents=prompt
            )
            return response.text
        except Exception as e:
            if "429" in str(e) and attempt == 0:
                time.sleep(10)
                continue 
            return f"⚠️ AI Error: {str(e)}"

def run_async(coro):
    return asyncio.run(coro)

# ==========================================
# 🖥️ 3. STREAMLIT COMMAND CENTER
# ==========================================
def main():
    st.set_page_config(page_title="Job Warrior Pro", page_icon="⚔️", layout="wide")
    
    # Custom CSS for a "War Room" feel
    st.markdown("""
        <style>
        .main { background-color: #0e1117; color: #fafafa; }
        .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; }
        </style>
        """, unsafe_allow_html=True)

    st.title("⚔️ Job Warrior — Command Center")
    st.caption("Scouting Pune for the best career opportunities.")

    # --- SIDEBAR ---
    with st.sidebar:
        st.header("👤 Warrior Profile")
        user_email = st.text_input("Your Contact Email", value="warrior@pune.com")
        user_experience = st.number_input("Years of Experience", 0, 40, 2)
        key_words = st.text_area("Keywords", "Python, SQL, Streamlit")
        st.divider()
        st.success("Profile Loaded")

    # --- MAIN CONTROLS ---
    with st.container(border=True):
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            job_query = st.text_input("Target Role", placeholder="e.g. Data Scientist")
        with col2:
            job_count = st.select_slider("Leads to Fetch", options=[1, 3, 5, 10], value=3)
        with col3:
            stealth_mode = st.toggle("Stealth Mode", value=True)
            st.caption("ON = Headless (Recommended)")

        if st.button("🚀 DEPLOY SCOUT"):
            if job_query:
                st.session_state.mission_active = True
                st.session_state.query = job_query
            else:
                st.error("Commander, specify a target role!")

    # --- RESULTS AREA ---
    if st.session_state.get("mission_active"):
        with st.status("Deploying Scout to the field...", expanded=True) as status:
            # 1. Scraping
            leads = run_async(auto_scout(st.session_state.query, stealth_mode, job_count))
            
            if leads and "No leads" not in leads[0]:
                st.subheader("📍 Scouting Results")
                for lead in leads:
                    st.write(f"🔹 {lead}")
                
                # 2. AI Analysis
                st.subheader("🧠 Intelligence Report")
                intel = {"email": user_email, "exp": user_experience, "skills": key_words}
                report = ai_analyze(st.session_state.query, leads, intel)
                st.info(report)
                
                # 3. Download Feature
                df = pd.DataFrame(leads, columns=["Job Lead"])
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📂 Download Intelligence Report (CSV)", csv, "leads.csv", "text/csv")
            else:
                st.error("Scout returned empty-handed. Try a simpler job title.")
            
            status.update(label="Mission Complete!", state="complete")

        if st.button("🔄 Reset Command Center"):
            st.session_state.mission_active = False
            st.rerun()

if __name__ == "__main__":
    main()