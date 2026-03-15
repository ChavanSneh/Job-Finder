# 🔍 Job Scout AI

Job Scout AI is an intelligent career assistant designed to bridge the gap between your unique skill set and the evolving Pune tech job market. Instead of keyword matching, this application uses Google’s Gemini 2.5 Flash model to semantically analyze job descriptions against your personal resume.

## ✨ Key Features

* **Semantic Job Matching:** Goes beyond keyword searching to understand the context of your experience (RAG, Agentic AI, Cloud infrastructure).
  
* **AI Career Consultant:** Leverages a custom system instruction to provide strategic advice, identifying experience gaps and suggesting targeted skill improvements.
  
* **Resilient Infrastructure:** Built with `tenacity` for automatic exponential backoff, ensuring your API requests recover gracefully from rate limits.
  
* **Resume-Driven Insights:** Parses your PDF resume to provide personalized match scores and actionable feedback.

## 🛠️ Tech Stack

* **Core:** Python 3.x
  
* **AI/LLM:** Google Gen AI SDK (`google-genai`), Gemini 2.5 Flash
  
* **Backend:** FastAPI
  
* **Data Processing:** Pydantic (Schema validation), Tenacity (Retry logic)
  
* **Frontend:** Streamlit

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
  
- A Google AI Studio API Key

### Installation

1. Clone the repository:
   
   git clone [https://github.com/your-username/job-scout-ai.git](https://github.com/your-username/job-scout-ai.git)
   cd job-scout-ai
   
Create and activate a virtual environment:

python -m venv venv

source venv/bin/activate  # Windows: venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Configure your environment:

Create a .env file in the root directory.

Add your API key: GEMINI_API_KEY=your_actual_api_key_here

Running the App

streamlit run app.py

🧠 Intelligence Engine

The core of the app is the ai_analyst.py module, which orchestrates the interaction between your profile and the market findings.

🤝 Contributing

Contributions are welcome! If you have ideas for adding new cloud providers, improving the resume parsing logic, or optimizing the prompt engineering, feel free to open a Pull Request.

📄 License

This project is open-source and available under the MIT License.
