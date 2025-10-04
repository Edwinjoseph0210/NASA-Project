#!/bin/bash

# AirAware Startup Script
# This script helps you get started with the AirAware application

set -e

echo "🌬️  Welcome to AirAware - Real-Time Air Quality Forecasting"
echo "=============================================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating environment configuration..."
    cp env.example .env
    echo "⚠️  Please edit .env file with your API keys before continuing"
    echo "   Required: AIRNOW_API_KEY, NASA_EARTHDATA_USERNAME, NASA_EARTHDATA_PASSWORD, MAPBOX_TOKEN"
    echo ""
    read -p "Press Enter after you've updated the .env file..."
fi

echo "🔧 Starting AirAware services..."

# Start the services
docker-compose up -d

echo "⏳ Waiting for services to start..."

# Wait for database to be ready
echo "📊 Waiting for database..."
sleep 10

# Wait for backend to be ready
echo "🔧 Waiting for backend..."
sleep 15

# Wait for frontend to be ready
echo "🌐 Waiting for frontend..."
sleep 10

echo ""
echo "🎉 AirAware is now running!"
echo ""
echo "📱 Access the application:"
echo "   Frontend:    http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs:    http://localhost:8000/docs"
echo ""
echo "📊 Monitor services:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 Stop services:"
echo "   docker-compose down"
echo ""
echo "📚 Documentation:"
echo "   README.md - Project overview"
echo "   DEPLOYMENT.md - Deployment guide"
echo "   API_DOCUMENTATION.md - API reference"
echo ""
echo "🔍 Check service status:"
docker-compose ps

echo ""
echo "✨ Happy forecasting! 🌬️"
