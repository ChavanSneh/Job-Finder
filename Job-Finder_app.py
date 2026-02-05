import streamlit as st
import google.generativeai as genai
import asyncio
from playwright.async_api import async_playwright
import os

# 🛡️ SILENCE THE NOISE
os.environ["PYTHONWARNINGS"] = "ignore"

# --- 1. BRAIN CONFIGURATION (Gemini) ---
# Pulling from your hidden .streamlit/secrets.toml
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("🚨 Boss, GOOGLE_API_KEY is missing from secrets.toml!")
    st.stop()

# --- 2. THE SCOUTER ENGINE (Playwright) ---
async def scrape_indeed(url):
    jobs = []
    async with async_playwright() as p:
        # Launching 'Ghost' browser for Linux/Codespaces
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            await page.goto(url, timeout=60000)
            # Find job links using the common Indeed pattern
            # Note: Indeed changes selectors often; this is the most stable 'anchor' strategy
            links = await page.query_selector_all('a[href*="/rc/clk"]')
            
            for link in links[:10]: # Scrape top 10 for speed
                title = await link.inner_text()
                href = await link.get_attribute("href")
                full_link = f"https://www.indeed.com{href}"
                
                if title and href:
                    jobs.append({"title": title, "link": full_link})
        except Exception as e:
            st.sidebar.error(f"Scouter Shielded: {e}")
        
        await browser.close()
    return jobs

# --- 3. STATE MANAGEMENT ---
if 'master_queue' not in st.session_state:
    st.session_state.master_queue = []
if 'shortlist' not in st.session_state:
    st.session_state.shortlist = []
if 'rejected_count' not in st.session_state:
    st.session_state.rejected_count = 0

# --- 4. THE UI DASHBOARD ---
st.title("⚔️ Job Warrior Factory")

with st.sidebar:
    st.header("📊 Warehouse Stats")
    col1, col2 = st.columns(2)
    col1.metric("📦 Units", len(st.session_state.master_queue))
    col2.metric("✅ Kept", len(st.session_state.shortlist))
    st.write(f"❌ Discarded: {st.session_state.rejected_count}")
    
    st.divider()
    
    # URL Input
    indeed_url = st.text_input("Paste Indeed Pune URL", placeholder="https://in.indeed.com/jobs?q=python...")
    
    if st.button("🚀 Start Auto-Scout"):
        if indeed_url:
            with st.spinner("🕵️ Scouter infiltrating Indeed..."):
                new_leads = asyncio.run(scrape_indeed(indeed_url))
                if new_leads:
                    st.session_state.master_queue.extend(new_leads)
                    st.success(f"Added {len(new_leads)} leads to Warehouse!")
                    st.rerun()
                else:
                    st.warning("No leads found. Check the URL or User-Agent.")
        else:
            st.error("Give me a URL first, Boss!")

# --- 5. THE REVIEW CONVEYOR BELT ---
if st.session_state.master_queue:
    current_job = st.session_state.master_queue[0]
    
    with st.container(border=True):
        st.subheader(f"🔍 Lead: {current_job['title']}")
        st.write(f"🔗 [View Full Posting]({current_job['link']})")
        
        c1, c2, c3 = st.columns(3)
        
        if c1.button("✅ Shortlist"):
            st.session_state.shortlist.append(current_job)
            st.session_state.master_queue.pop(0)
            st.toast("Unit moved to Shortlist!", icon="✅")
            st.rerun()
            
        if c2.button("❌ Reject"):
            st.session_state.rejected_count += 1
            st.session_state.master_queue.pop(0)
            st.toast("Unit discarded.", icon="🗑️")
            st.rerun()

        if c3.button("⏭️ Skip"):
            st.session_state.master_queue.append(st.session_state.master_queue.pop(0))
            st.rerun()

else:
    st.info("Warehouse is empty. Use the sidebar to scout for new leads! 🧘‍♂️")

# --- 6. VIEW SHORTLIST ---
if st.session_state.shortlist:
    with st.expander("📝 View My Shortlist"):
        for item in st.session_state.shortlist:
            st.write(f"- {item['title']} ([Link]({item['link']}))")