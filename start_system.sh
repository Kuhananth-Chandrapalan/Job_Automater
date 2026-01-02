#!/bin/bash

GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}🚀 Starting Job Automation System...${NC}"

# 1. Setup Venv & Install Deps
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    ./venv/bin/pip install -U pip
fi

echo "📦 Syncing Python dependencies..."
./venv/bin/pip install -r requirements.txt

# 2. Start n8n (Docker)
echo "🐳 Starting n8n container..."
sudo docker compose up -d
echo "   -> n8n Dashboard: http://localhost:5678"

# 3. Start Intelligence API
echo -e "${GREEN}🧠 Starting Intelligence Microservice (API)...${NC}"
echo "   -> Listening on http://localhost:8010"
echo "   (Press Ctrl+C to stop the API)"

./venv/bin/python -m uvicorn src.api:app --host 0.0.0.0 --port 8010 --reload
