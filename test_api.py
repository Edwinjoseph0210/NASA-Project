#!/usr/bin/env python3
"""
Simple test script for Ernakulam Air Quality Monitor API
Run this after starting the server to test all endpoints
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_root():
    """Test root endpoint"""
    print_section("Testing Root Endpoint")
    response = requests.get(f"{BASE_URL}/")
    data = response.json()
    print(f"Message: {data['message']}")
    print(f"District: {data['district']}")
    print(f"Version: {data['version']}")
    print("\nAvailable Endpoints:")
    for name, path in data['endpoints'].items():
        print(f"  - {name}: {path}")

def test_health():
    """Test health check endpoint"""
    print_section("Testing Health Check")
    response = requests.get(f"{BASE_URL}/health")
    data = response.json()
    print(f"Status: {data['status']}")
    print(f"Timestamp: {data['timestamp']}")

def test_district_summary():
    """Test district summary endpoint"""
    print_section("Testing District Summary")
    response = requests.get(f"{BASE_URL}/api/summary")
    data = response.json()
    
    print(f"District: {data['district']}")
    print(f"Overall AQI: {data['overall_aqi']} ({data['aqi_category']})")
    print(f"\nHealth Advisory:")
    print(f"  {data['health_advisory']}")
    
    print(f"\nAverage Pollutant Levels:")
    print(f"  PM2.5: {data['averages']['pm25']} μg/m³")
    print(f"  PM10:  {data['averages']['pm10']} μg/m³")
    print(f"  NO2:   {data['averages']['no2']} μg/m³")
    
    print(f"\nWorst Location: {data['worst_location']['name']} (AQI: {data['worst_location']['aqi']})")
    print(f"Best Location:  {data['best_location']['name']} (AQI: {data['best_location']['aqi']})")
    print(f"\nTotal Monitoring Stations: {data['total_stations']}")

def test_all_stations():
    """Test all stations endpoint"""
    print_section("Testing All Stations")
    response = requests.get(f"{BASE_URL}/api/stations")
    data = response.json()
    
    print(f"District: {data['district']}")
    print(f"Total Stations: {data['total_stations']}")
    print(f"\nStation Details:")
    
    for station in data['stations']:
        print(f"\n  📍 {station['station_name']} ({station['station_id']})")
        print(f"     Location: {station['location']}")
        print(f"     Coordinates: {station['latitude']}, {station['longitude']}")
        print(f"     AQI: {station['aqi']} ({station['aqi_category']})")
        print(f"     PM2.5: {station['pollutants']['pm25']} μg/m³")

def test_station_detail():
    """Test individual station endpoint"""
    print_section("Testing Station Detail (Kochi City Center)")
    station_id = "EKM001"
    response = requests.get(f"{BASE_URL}/api/stations/{station_id}")
    data = response.json()
    
    print(f"Station: {data['station_name']} ({data['station_id']})")
    print(f"Location: {data['location']}")
    print(f"AQI: {data['aqi']} ({data['aqi_category']})")
    
    print(f"\nPollutant Levels:")
    for pollutant, value in data['pollutants'].items():
        print(f"  {pollutant.upper()}: {value}")
    
    print(f"\nHealth Advisory:")
    print(f"  {data['health_advisory']}")

def test_station_history():
    """Test station history endpoint"""
    print_section("Testing Station History (24 hours)")
    station_id = "EKM002"
    response = requests.get(f"{BASE_URL}/api/stations/{station_id}/history?hours=24")
    data = response.json()
    
    print(f"Station ID: {data['station_id']}")
    print(f"Hours of data: {data['hours']}")
    print(f"Total data points: {data['data_points']}")
    
    if data['data']:
        latest = data['data'][-1]
        oldest = data['data'][0]
        print(f"\nLatest reading:")
        print(f"  Time: {latest['timestamp']}")
        print(f"  AQI: {latest['aqi']} ({latest['aqi_category']})")
        print(f"  PM2.5: {latest['pollutants']['pm25']} μg/m³")

def test_station_forecast():
    """Test station forecast endpoint"""
    print_section("Testing Station Forecast (24 hours)")
    station_id = "EKM003"
    response = requests.get(f"{BASE_URL}/api/stations/{station_id}/forecast?hours=24")
    data = response.json()
    
    print(f"Station ID: {data['station_id']}")
    print(f"Forecast hours: {data['forecast_hours']}")
    print(f"Total forecast points: {data['data_points']}")
    print(f"Note: {data['note']}")
    
    if data['forecast']:
        first = data['forecast'][0]
        print(f"\nNext hour forecast:")
        print(f"  Time: {first['timestamp']}")
        print(f"  Predicted AQI: {first['aqi']} ({first['aqi_category']})")
        print(f"  Predicted PM2.5: {first['pollutants']['pm25']} μg/m³")

def main():
    """Run all tests"""
    print("\n" + "🌍 " * 20)
    print("  ERNAKULAM AIR QUALITY MONITOR - API TEST SUITE")
    print("🌍 " * 20)
    
    try:
        test_root()
        test_health()
        test_district_summary()
        test_all_stations()
        test_station_detail()
        test_station_history()
        test_station_forecast()
        
        print_section("✅ All Tests Completed Successfully!")
        print("\nThe API is working correctly!")
        print("\nTry these URLs in your browser:")
        print(f"  - API Docs: {BASE_URL}/docs")
        print(f"  - District Summary: {BASE_URL}/api/summary")
        print(f"  - All Stations: {BASE_URL}/api/stations")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to the API server!")
        print("Please make sure the server is running:")
        print("  ./start-ernakulam.sh")
        print("or:")
        print("  cd backend && python main.py")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
