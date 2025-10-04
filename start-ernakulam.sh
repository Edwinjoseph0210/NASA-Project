#!/bin/bash

echo "======================================"
echo "Ernakulam Air Quality Monitor"
echo "======================================"
echo ""
echo "Starting the API server..."
echo ""

cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements-simple.txt

echo ""
echo "======================================"
echo "Starting Ernakulam Air Quality Monitor API"
echo "======================================"
echo ""
echo "API will be available at:"
echo "  - Main API: http://localhost:8000"
echo "  - Documentation: http://localhost:8000/docs"
echo "  - District Summary: http://localhost:8000/api/summary"
echo ""
echo "Monitoring 6 stations in Ernakulam district:"
echo "  1. Kochi City Center (EKM001)"
echo "  2. Kakkanad IT Park (EKM002)"
echo "  3. Fort Kochi (EKM003)"
echo "  4. Aluva (EKM004)"
echo "  5. Thrippunithura (EKM005)"
echo "  6. Edappally (EKM006)"
echo ""
echo "Press Ctrl+C to stop the server"
echo "======================================"
echo ""

# Run the application
python main.py
