🔍 AI Job Scout: AI-Powered Career Intelligence
A high-performance career intelligence tool built with FastAPI, Google Gemini AI, and Streamlit. This tool automates the search and strategic analysis of job listings, turning "quantity" from API results into "quality" actionable career insights.

🚀 Features
AI-Native Analysis: Utilizes gemini-2.5-flash to evaluate job fit based on your resume and skills.

Smart Aggregation: API-driven pipeline for fast, reliable job data retrieval.

Interactive Dashboard: Modern UI built with Streamlit for real-time job exploration.

Persistent Profile: Keeps your skills, experience, and career goals saved for automated matching.

🛠️ Tech Stack
Backend: Python 3.12+, FastAPI

AI: Google Generative AI SDK

Frontend: Streamlit

Environment: WSL (Ubuntu) / Windows

📦 Installation & Setup
1. Clone & Setup
Bash
git clone https://github.com/ChavanSneh/Job-Finder.git
cd Job-Finder
2. Environment Setup
Create and activate your virtual environment:

For WSL/Linux:

Bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
For Windows:

Bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
3. API Configuration
Create a .env file in the root directory and add your Google Gemini API Key:

Plaintext
GEMINI_API_KEY=your_actual_api_key_here
Note: Ensure this file is never committed to GitHub.

⚔️ Usage
Launch the system using the provided scripts:

For WSL/Linux:

Bash
chmod +x run_app.sh
./run_app.sh
For Windows:

Bash
start_app.bat
Open your browser to http://localhost:8501 to start analyzing roles.

📊 How it Works
Job Acquisition: The JSearchProvider fetches relevant listings based on your profile.

AI Intelligence: The analyze_jobs module sends data to Gemini with custom system instructions.

Strategic Output: The AI returns a strategic summary, matching your experience against job requirements.

Developed by Chavan Sneh