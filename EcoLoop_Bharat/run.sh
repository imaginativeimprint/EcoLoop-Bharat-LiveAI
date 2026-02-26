#!/bin/bash

# EcoLoop Bharat Startup Script
echo "🚀 Starting EcoLoop Bharat..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python version
python_version=$(python3 --version 2>&1 | grep -Po '(?<=Python )\d+\.\d+')
if (( $(echo "$python_version < 3.10" | bc -l) )); then
    echo -e "${RED}❌ Python 3.10+ required (found $python_version)${NC}"
    exit 1
fi

# Install dependencies
echo -e "${YELLOW}📦 Installing dependencies...${NC}"
pip install -r requirements.txt

# Generate mock data
echo -e "${YELLOW}📊 Generating mock data...${NC}"
python data/mock_data_generator.py

# Create live data directory
mkdir -p data/live

# Start Pathway processor in background
echo -e "${YELLOW}⚙️ Starting Pathway engine...${NC}"
python engine/processor.py &
PATHWAY_PID=$!

# Wait for Pathway to initialize
sleep 3

# Start Streamlit dashboard
echo -e "${GREEN}✅ Dashboard available at http://localhost:8501${NC}"
echo -e "${YELLOW}📊 Launching dashboard...${NC}"
streamlit run ui/dashboard.py --server.port 8501

# Cleanup on exit
trap "kill $PATHWAY_PID" EXIT