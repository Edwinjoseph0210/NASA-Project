"""
Simplified data service for Ernakulam district air quality monitoring
"""
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

# Key locations in Ernakulam district
ERNAKULAM_STATIONS = [
    {
        "station_id": "EKM001",
        "name": "Kochi City Center",
        "latitude": 9.9312,
        "longitude": 76.2673,
        "location": "MG Road, Kochi",
        "type": "urban"
    },
    {
        "station_id": "EKM002",
        "name": "Kakkanad IT Park",
        "latitude": 10.0104,
        "longitude": 76.3497,
        "location": "Infopark, Kakkanad",
        "type": "industrial"
    },
    {
        "station_id": "EKM003",
        "name": "Fort Kochi",
        "latitude": 9.9654,
        "longitude": 76.2424,
        "location": "Fort Kochi Beach",
        "type": "coastal"
    },
    {
        "station_id": "EKM004",
        "name": "Aluva",
        "latitude": 10.1081,
        "longitude": 76.3522,
        "location": "Aluva Metro Station",
        "type": "urban"
    },
    {
        "station_id": "EKM005",
        "name": "Thrippunithura",
        "latitude": 9.9447,
        "longitude": 76.3478,
        "location": "Hill Palace Road",
        "type": "residential"
    },
    {
        "station_id": "EKM006",
        "name": "Edappally",
        "latitude": 10.0242,
        "longitude": 76.3084,
        "location": "NH Bypass, Edappally",
        "type": "traffic"
    }
]


class ErnakulamDataService:
    """Service for managing Ernakulam air quality data"""
    
    def __init__(self):
        self.stations = ERNAKULAM_STATIONS
        self.data_cache = {}
    
    def get_stations(self) -> List[Dict[str, Any]]:
        """Get all monitoring stations in Ernakulam"""
        return self.stations
    
    def get_station_by_id(self, station_id: str) -> Dict[str, Any]:
        """Get a specific station by ID"""
        for station in self.stations:
            if station["station_id"] == station_id:
                return station
        return None
    
    def generate_mock_reading(self, station: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate realistic mock air quality data for a station
        Based on typical pollution patterns in Kerala cities
        """
        # Base pollution levels vary by station type
        base_levels = {
            "urban": {"pm25": 45, "pm10": 75, "no2": 35, "o3": 40, "so2": 15, "co": 0.8},
            "industrial": {"pm25": 65, "pm10": 95, "no2": 50, "o3": 45, "so2": 25, "co": 1.2},
            "coastal": {"pm25": 30, "pm10": 55, "no2": 25, "o3": 50, "so2": 10, "co": 0.5},
            "residential": {"pm25": 40, "pm10": 70, "no2": 30, "o3": 35, "so2": 12, "co": 0.7},
            "traffic": {"pm25": 70, "pm10": 105, "no2": 60, "o3": 30, "so2": 20, "co": 1.5}
        }
        
        station_type = station.get("type", "urban")
        base = base_levels.get(station_type, base_levels["urban"])
        
        # Add time-based variation (higher pollution during peak hours)
        hour = datetime.now().hour
        time_factor = 1.0
        if 7 <= hour <= 10 or 17 <= hour <= 20:  # Peak traffic hours
            time_factor = 1.3
        elif 0 <= hour <= 5:  # Night hours
            time_factor = 0.7
        
        # Add random variation
        reading = {
            "pm25": round(base["pm25"] * time_factor * random.uniform(0.8, 1.2), 2),
            "pm10": round(base["pm10"] * time_factor * random.uniform(0.8, 1.2), 2),
            "no2": round(base["no2"] * time_factor * random.uniform(0.8, 1.2), 2),
            "o3": round(base["o3"] * time_factor * random.uniform(0.8, 1.2), 2),
            "so2": round(base["so2"] * time_factor * random.uniform(0.8, 1.2), 2),
            "co": round(base["co"] * time_factor * random.uniform(0.8, 1.2), 2)
        }
        
        # Calculate AQI (simplified US EPA formula for PM2.5)
        aqi = self.calculate_aqi(reading["pm25"])
        
        return {
            "station_id": station["station_id"],
            "station_name": station["name"],
            "location": station["location"],
            "latitude": station["latitude"],
            "longitude": station["longitude"],
            "timestamp": datetime.utcnow().isoformat(),
            "pollutants": reading,
            "aqi": aqi,
            "aqi_category": self.get_aqi_category(aqi),
            "health_advisory": self.get_health_advisory(aqi)
        }
    
    def calculate_aqi(self, pm25: float) -> int:
        """
        Calculate AQI from PM2.5 concentration (simplified US EPA formula)
        """
        if pm25 <= 12.0:
            return int((50 / 12.0) * pm25)
        elif pm25 <= 35.4:
            return int(50 + ((100 - 50) / (35.4 - 12.1)) * (pm25 - 12.1))
        elif pm25 <= 55.4:
            return int(100 + ((150 - 100) / (55.4 - 35.5)) * (pm25 - 35.5))
        elif pm25 <= 150.4:
            return int(150 + ((200 - 150) / (150.4 - 55.5)) * (pm25 - 55.5))
        elif pm25 <= 250.4:
            return int(200 + ((300 - 200) / (250.4 - 150.5)) * (pm25 - 150.5))
        else:
            return int(300 + ((500 - 300) / (500.4 - 250.5)) * (pm25 - 250.5))
    
    def get_aqi_category(self, aqi: int) -> str:
        """Get AQI category from AQI value"""
        if aqi <= 50:
            return "Good"
        elif aqi <= 100:
            return "Moderate"
        elif aqi <= 150:
            return "Unhealthy for Sensitive Groups"
        elif aqi <= 200:
            return "Unhealthy"
        elif aqi <= 300:
            return "Very Unhealthy"
        else:
            return "Hazardous"
    
    def get_health_advisory(self, aqi: int) -> str:
        """Get health advisory based on AQI"""
        if aqi <= 50:
            return "Air quality is satisfactory, and air pollution poses little or no risk."
        elif aqi <= 100:
            return "Air quality is acceptable. However, there may be a risk for some people, particularly those who are unusually sensitive to air pollution."
        elif aqi <= 150:
            return "Members of sensitive groups may experience health effects. The general public is less likely to be affected."
        elif aqi <= 200:
            return "Some members of the general public may experience health effects; members of sensitive groups may experience more serious health effects."
        elif aqi <= 300:
            return "Health alert: The risk of health effects is increased for everyone."
        else:
            return "Health warning of emergency conditions: everyone is more likely to be affected."
    
    def get_current_readings(self) -> List[Dict[str, Any]]:
        """Get current readings for all stations"""
        readings = []
        for station in self.stations:
            reading = self.generate_mock_reading(station)
            readings.append(reading)
        return readings
    
    def get_station_reading(self, station_id: str) -> Dict[str, Any]:
        """Get current reading for a specific station"""
        station = self.get_station_by_id(station_id)
        if not station:
            return None
        return self.generate_mock_reading(station)
    
    def get_historical_data(self, station_id: str, hours: int = 24) -> List[Dict[str, Any]]:
        """
        Generate historical data for a station
        (In production, this would fetch from database)
        """
        station = self.get_station_by_id(station_id)
        if not station:
            return []
        
        historical_data = []
        current_time = datetime.utcnow()
        
        # Generate data points for each hour
        for i in range(hours):
            timestamp = current_time - timedelta(hours=i)
            reading = self.generate_mock_reading(station)
            reading["timestamp"] = timestamp.isoformat()
            historical_data.append(reading)
        
        return list(reversed(historical_data))
    
    def get_forecast(self, station_id: str, hours: int = 24) -> List[Dict[str, Any]]:
        """
        Generate simple forecast data
        (In production, this would use ML models)
        """
        station = self.get_station_by_id(station_id)
        if not station:
            return []
        
        forecast_data = []
        current_time = datetime.utcnow()
        
        # Generate forecast for next N hours
        for i in range(1, hours + 1):
            timestamp = current_time + timedelta(hours=i)
            reading = self.generate_mock_reading(station)
            reading["timestamp"] = timestamp.isoformat()
            reading["is_forecast"] = True
            forecast_data.append(reading)
        
        return forecast_data
    
    def get_district_summary(self) -> Dict[str, Any]:
        """Get overall air quality summary for Ernakulam district"""
        readings = self.get_current_readings()
        
        if not readings:
            return {"error": "No data available"}
        
        # Calculate district averages
        total_aqi = sum(r["aqi"] for r in readings)
        avg_aqi = int(total_aqi / len(readings))
        
        avg_pm25 = sum(r["pollutants"]["pm25"] for r in readings) / len(readings)
        avg_pm10 = sum(r["pollutants"]["pm10"] for r in readings) / len(readings)
        avg_no2 = sum(r["pollutants"]["no2"] for r in readings) / len(readings)
        
        # Find worst and best stations
        worst_station = max(readings, key=lambda x: x["aqi"])
        best_station = min(readings, key=lambda x: x["aqi"])
        
        return {
            "district": "Ernakulam",
            "timestamp": datetime.utcnow().isoformat(),
            "overall_aqi": avg_aqi,
            "aqi_category": self.get_aqi_category(avg_aqi),
            "health_advisory": self.get_health_advisory(avg_aqi),
            "averages": {
                "pm25": round(avg_pm25, 2),
                "pm10": round(avg_pm10, 2),
                "no2": round(avg_no2, 2)
            },
            "worst_location": {
                "name": worst_station["station_name"],
                "aqi": worst_station["aqi"]
            },
            "best_location": {
                "name": best_station["station_name"],
                "aqi": best_station["aqi"]
            },
            "total_stations": len(readings),
            "stations": readings
        }
