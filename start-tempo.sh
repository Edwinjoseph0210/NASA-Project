#!/bin/bash

echo "=========================================="
echo "🛰️  NASA TEMPO Air Quality Monitor"
echo "=========================================="
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
pip install -q -r requirements-tempo.txt

echo ""
echo "=========================================="
echo "NASA TEMPO Air Quality Monitor API"
echo "=========================================="
echo ""
echo "🌍 Coverage: North America"
echo "🛰️  Satellite: NASA TEMPO (Geostationary)"
echo "📡 Resolution: Hourly, ~10km spatial"
echo ""
echo "API will be available at:"
echo "  - Main API: http://localhost:8000"
echo "  - Documentation: http://localhost:8000/docs"
echo "  - Summary: http://localhost:8000/api/summary"
echo ""
echo "Monitoring 10 major cities:"
echo "  🇺🇸 USA:"
echo "    - New York City (NYC001)"
echo "    - Los Angeles (LAX001)"
echo "    - Chicago (CHI001)"
echo "    - Houston (HOU001)"
echo "    - Phoenix (PHX001)"
echo "    - Miami (MIA001)"
echo "    - Seattle (SEA001)"
echo "    - Denver (DEN001)"
echo "  🇨🇦 Canada:"
echo "    - Toronto (TOR001)"
echo "  🇲🇽 Mexico:"
echo "    - Mexico City (MEX001)"
echo ""
echo "Dashboard: Open dashboard-tempo.html in your browser"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

# Run the application
python main.py
