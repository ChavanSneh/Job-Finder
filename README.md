Here is an updated README.md that incorporates your new backend-frontend architecture, the environment setup, and the convenient one-click runners for both Windows and WSL.

🔍 AI Job Scout: Python Automation Tool
A next-gen job intelligence tool built with FastAPI, Gemini AI, and Streamlit to streamline the job search process using real-time AI insights.

🚀 Features
AI Job Intelligence: Analyzes job descriptions using Google Gemini.

Automated Backend: High-performance FastAPI orchestration.

Interactive UI: Modern web interface built with Streamlit.

Resume Analysis: PDF parsing for tailored job matching.

🛠️ Tech Stack
Language: Python 3.12+

Backend: FastAPI

AI: Google Generative AI (Gemini)

Frontend: Streamlit

Environment: WSL (Ubuntu) / Windows

📦 Installation & Setup
1. Clone & Navigate
Bash
git clone https://github.com/ChavanSneh/Job-Finder.git
cd Job-Finder
2. Environment Setup
Create a virtual environment to manage dependencies:

For WSL / Linux:

Bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
For Windows (Command Prompt/PowerShell):

Bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
3. API Configuration
Create a .env file in the root directory and add your Google Gemini API Key:

Plaintext
GEMINI_API_KEY=your_actual_api_key_here
⚔️ Usage
We have simplified the startup process so you can launch the entire system from the root directory.

Launching the Application
For WSL (Linux shell):
Run the shell script:

Bash
chmod +x run_app.sh
./run_app.sh
For Windows (Batch file):
Simply double-click start_app.bat or run it from your terminal:

Bash
start_app.bat
Script Contents
Your run_app.sh (WSL) and start_app.bat (Windows) should contain the following logic to ensure the backend and frontend start concurrently:

Developed by Chavan Sneh