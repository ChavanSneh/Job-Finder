#!/bin/bash
echo "Starting Job Scout AI..."

# Start backend using the module path
python3 -m uvicorn backend.app:app --reload &

# Start frontend using the correct filename
streamlit run frontend/streamlit_app.py