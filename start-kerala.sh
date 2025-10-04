#!/bin/bash

# AirAware Kerala Startup Script
# Focused on Kottayam, Kerala region

set -e

echo "🌴 Welcome to AirAware Kerala - Air Quality Monitoring for Kottayam"
echo "=================================================================="

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
    echo "✅ Environment file created with demo settings"
fi

echo "🔧 Starting AirAware Kerala services..."

# Start the Kerala-specific services
docker-compose -f docker-compose-kerala.yml up -d

echo "⏳ Waiting for services to start..."

# Wait for database to be ready
echo "📊 Waiting for Kerala database..."
sleep 10

# Wait for backend to be ready
echo "🔧 Waiting for Kerala backend..."
sleep 15

# Wait for frontend to be ready
echo "🌐 Waiting for Kerala frontend..."
sleep 10

echo ""
echo "🎉 AirAware Kerala is now running!"
echo ""
echo "📱 Access the Kerala application:"
echo "   Frontend:    http://localhost:3000/kerala"
echo "   Backend API: http://localhost:8000"
echo "   API Docs:    http://localhost:8000/docs"
echo ""
echo "🌴 Kerala Features:"
echo "   • 8 monitoring stations in Kerala"
echo "   • Focused on Kottayam region"
echo "   • Real-time air quality data"
echo "   • 24-hour forecasts"
echo "   • Local alerts and notifications"
echo ""
echo "📊 Monitor services:"
echo "   docker-compose -f docker-compose-kerala.yml logs -f"
echo ""
echo "🛑 Stop services:"
echo "   docker-compose -f docker-compose-kerala.yml down"
echo ""
echo "🔍 Check service status:"
docker-compose -f docker-compose-kerala.yml ps

echo ""
echo "✨ Enjoy monitoring Kerala's air quality! 🌴🌬️"
