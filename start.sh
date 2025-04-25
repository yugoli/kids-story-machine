#!/bin/bash

# Activate your environment
source venv/bin/activate

# Start Backend
echo "Starting backend..."
cd backend
uvicorn app.main:app --reload &
BACKEND_PID=$!
cd ..

# Start Frontend
echo "Starting frontend..."
cd frontend
streamlit run app.py

# When you exit streamlit, kill backend
kill $BACKEND_PID
