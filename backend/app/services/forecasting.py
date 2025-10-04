import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from sqlalchemy.orm import Session
import joblib
import os

from app.core.config import settings
from app.models.air_quality import AirQualityReading, AirQualityStation, WeatherData, TEMPOData, ForecastModel
from app.schemas import ForecastDataPoint, AirQualityParameter

logger = logging.getLogger(__name__)

class ForecastingService:
    """Service for air quality forecasting using ML models"""
    
    def __init__(self):
        self.models = {}
        self.model_path = settings.ML_MODEL_PATH
        
    async def initialize(self):
        """Initialize forecasting models"""
        try:
            # Load available models
            await self._load_models()
            logger.info("Forecasting service initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing forecasting service: {str(e)}")
    
    async def _load_models(self):
        """Load ML models from disk"""
        try:
            if not os.path.exists(self.model_path):
                os.makedirs(self.model_path, exist_ok=True)
                logger.warning(f"Model directory created: {self.model_path}")
                return
            
            # Load models for different parameters
            parameters = ["pm25", "o3", "no2", "aqi"]
            
            for param in parameters:
                model_file = os.path.join(self.model_path, f"{param}_model.pkl")
                if os.path.exists(model_file):
                    try:
                        self.models[param] = joblib.load(model_file)
                        logger.info(f"Loaded model for {param}")
                    except Exception as e:
                        logger.error(f"Error loading model for {param}: {str(e)}")
                else:
                    logger.warning(f"Model file not found for {param}: {model_file}")
                    
        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")
    
    async def generate_forecast(
        self,
        latitude: float,
        longitude: float,
        forecast_hours: int = 24,
        include_confidence: bool = False
    ) -> Dict[str, Any]:
        """Generate air quality forecast for a location"""
        try:
            # Get historical data for the location
            historical_data = await self._get_historical_data(latitude, longitude)
            
            if not historical_data:
                # Return default forecast if no historical data
                return await self._generate_default_forecast(forecast_hours)
            
            # Prepare features for ML model
            features = await self._prepare_features(historical_data, latitude, longitude)
            
            # Generate forecasts for each parameter
            forecast_data = []
            
            for hour in range(forecast_hours):
                forecast_time = datetime.utcnow() + timedelta(hours=hour)
                
                # Generate forecast for this hour
                forecast_point = await self._generate_single_forecast(
                    features, forecast_time, include_confidence
                )
                
                forecast_data.append(forecast_point)
            
            # Get model information
            model_info = await self._get_model_info()
            
            return {
                "forecast_data": forecast_data,
                "model_info": model_info,
                "data_sources": ["airnow", "tempo", "weather"]
            }
            
        except Exception as e:
            logger.error(f"Error generating forecast: {str(e)}")
            return await self._generate_default_forecast(forecast_hours)
    
    async def _get_historical_data(
        self,
        latitude: float,
        longitude: float,
        days_back: int = 7
    ) -> Dict[str, List]:
        """Get historical air quality and weather data for a location"""
        try:
            # This would typically query the database
            # For now, return mock data structure
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=days_back)
            
            # Mock historical data structure
            historical_data = {
                "air_quality": [],
                "weather": [],
                "tempo": []
            }
            
            # Generate mock historical data
            for i in range(days_back * 24):  # Hourly data
                timestamp = start_time + timedelta(hours=i)
                
                # Mock air quality data
                historical_data["air_quality"].append({
                    "timestamp": timestamp,
                    "pm25": np.random.normal(15, 5),
                    "o3": np.random.normal(40, 10),
                    "no2": np.random.normal(20, 5),
                    "aqi": np.random.randint(30, 80)
                })
                
                # Mock weather data
                historical_data["weather"].append({
                    "timestamp": timestamp,
                    "temperature": np.random.normal(20, 5),
                    "humidity": np.random.normal(60, 15),
                    "wind_speed": np.random.normal(5, 2),
                    "pressure": np.random.normal(1013, 10)
                })
            
            return historical_data
            
        except Exception as e:
            logger.error(f"Error getting historical data: {str(e)}")
            return {}
    
    async def _prepare_features(
        self,
        historical_data: Dict[str, List],
        latitude: float,
        longitude: float
    ) -> np.ndarray:
        """Prepare features for ML model"""
        try:
            # Convert to DataFrame for easier processing
            df_aq = pd.DataFrame(historical_data["air_quality"])
            df_weather = pd.DataFrame(historical_data["weather"])
            
            # Merge dataframes on timestamp
            df = pd.merge(df_aq, df_weather, on="timestamp", how="outer")
            df = df.sort_values("timestamp")
            
            # Create time-based features
            df["hour"] = df["timestamp"].dt.hour
            df["day_of_week"] = df["timestamp"].dt.dayofweek
            df["month"] = df["timestamp"].dt.month
            
            # Create lag features
            for lag in [1, 2, 3, 6, 12, 24]:
                df[f"pm25_lag_{lag}"] = df["pm25"].shift(lag)
                df[f"o3_lag_{lag}"] = df["o3"].shift(lag)
                df[f"no2_lag_{lag}"] = df["no2"].shift(lag)
            
            # Create rolling averages
            for window in [3, 6, 12]:
                df[f"pm25_ma_{window}"] = df["pm25"].rolling(window=window).mean()
                df[f"o3_ma_{window}"] = df["o3"].rolling(window=window).mean()
                df[f"no2_ma_{window}"] = df["no2"].rolling(window=window).mean()
            
            # Add location features
            df["latitude"] = latitude
            df["longitude"] = longitude
            
            # Select features for model
            feature_columns = [
                "hour", "day_of_week", "month",
                "temperature", "humidity", "wind_speed", "pressure",
                "latitude", "longitude"
            ]
            
            # Add lag features
            lag_columns = [col for col in df.columns if "lag_" in col or "ma_" in col]
            feature_columns.extend(lag_columns)
            
            # Get the most recent row for prediction
            latest_features = df[feature_columns].iloc[-1:].values
            
            return latest_features
            
        except Exception as e:
            logger.error(f"Error preparing features: {str(e)}")
            return np.array([])
    
    async def _generate_single_forecast(
        self,
        features: np.ndarray,
        forecast_time: datetime,
        include_confidence: bool
    ) -> ForecastDataPoint:
        """Generate forecast for a single time point"""
        try:
            forecast_point = ForecastDataPoint(timestamp=forecast_time)
            
            # Generate forecasts for each parameter
            parameters = ["pm25", "o3", "no2"]
            
            for param in parameters:
                if param in self.models and len(features) > 0:
                    try:
                        # Make prediction
                        prediction = self.models[param].predict(features)
                        setattr(forecast_point, param, float(prediction[0]))
                        
                        # Calculate confidence intervals if requested
                        if include_confidence:
                            # This would typically use model uncertainty estimation
                            confidence_range = prediction[0] * 0.2  # 20% uncertainty
                            forecast_point.confidence_lower = float(prediction[0] - confidence_range)
                            forecast_point.confidence_upper = float(prediction[0] + confidence_range)
                            
                    except Exception as e:
                        logger.error(f"Error predicting {param}: {str(e)}")
                        # Use default values
                        setattr(forecast_point, param, self._get_default_value(param))
                else:
                    # Use default values if no model available
                    setattr(forecast_point, param, self._get_default_value(param))
            
            # Calculate AQI
            forecast_point.aqi = await self._calculate_aqi(forecast_point)
            
            return forecast_point
            
        except Exception as e:
            logger.error(f"Error generating single forecast: {str(e)}")
            return ForecastDataPoint(
                timestamp=forecast_time,
                pm25=self._get_default_value("pm25"),
                o3=self._get_default_value("o3"),
                no2=self._get_default_value("no2"),
                aqi=50
            )
    
    async def _calculate_aqi(self, forecast_point: ForecastDataPoint) -> int:
        """Calculate Air Quality Index from pollutant concentrations"""
        try:
            # AQI calculation based on EPA standards
            aqi_values = []
            
            # PM2.5 AQI
            if forecast_point.pm25:
                pm25_aqi = self._calculate_pm25_aqi(forecast_point.pm25)
                aqi_values.append(pm25_aqi)
            
            # O3 AQI
            if forecast_point.o3:
                o3_aqi = self._calculate_o3_aqi(forecast_point.o3)
                aqi_values.append(o3_aqi)
            
            # NO2 AQI
            if forecast_point.no2:
                no2_aqi = self._calculate_no2_aqi(forecast_point.no2)
                aqi_values.append(no2_aqi)
            
            # Return the maximum AQI value
            return max(aqi_values) if aqi_values else 50
            
        except Exception as e:
            logger.error(f"Error calculating AQI: {str(e)}")
            return 50
    
    def _calculate_pm25_aqi(self, pm25: float) -> int:
        """Calculate PM2.5 AQI"""
        if pm25 <= 12.0:
            return int(50 * pm25 / 12.0)
        elif pm25 <= 35.4:
            return int(50 + 50 * (pm25 - 12.0) / (35.4 - 12.0))
        elif pm25 <= 55.4:
            return int(100 + 50 * (pm25 - 35.4) / (55.4 - 35.4))
        elif pm25 <= 150.4:
            return int(150 + 50 * (pm25 - 55.4) / (150.4 - 55.4))
        elif pm25 <= 250.4:
            return int(200 + 50 * (pm25 - 150.4) / (250.4 - 150.4))
        else:
            return int(300 + 200 * (pm25 - 250.4) / (500.4 - 250.4))
    
    def _calculate_o3_aqi(self, o3: float) -> int:
        """Calculate O3 AQI (8-hour average)"""
        if o3 <= 0.054:
            return int(50 * o3 / 0.054)
        elif o3 <= 0.070:
            return int(50 + 50 * (o3 - 0.054) / (0.070 - 0.054))
        elif o3 <= 0.085:
            return int(100 + 50 * (o3 - 0.070) / (0.085 - 0.070))
        elif o3 <= 0.105:
            return int(150 + 50 * (o3 - 0.085) / (0.105 - 0.085))
        elif o3 <= 0.200:
            return int(200 + 100 * (o3 - 0.105) / (0.200 - 0.105))
        else:
            return int(300 + 200 * (o3 - 0.200) / (0.500 - 0.200))
    
    def _calculate_no2_aqi(self, no2: float) -> int:
        """Calculate NO2 AQI"""
        if no2 <= 0.053:
            return int(50 * no2 / 0.053)
        elif no2 <= 0.100:
            return int(50 + 50 * (no2 - 0.053) / (0.100 - 0.053))
        elif no2 <= 0.360:
            return int(100 + 50 * (no2 - 0.100) / (0.360 - 0.100))
        elif no2 <= 0.649:
            return int(150 + 50 * (no2 - 0.360) / (0.649 - 0.360))
        elif no2 <= 1.249:
            return int(200 + 100 * (no2 - 0.649) / (1.249 - 0.649))
        else:
            return int(300 + 200 * (no2 - 1.249) / (2.049 - 1.249))
    
    def _get_default_value(self, parameter: str) -> float:
        """Get default value for a parameter"""
        defaults = {
            "pm25": 15.0,
            "o3": 40.0,
            "no2": 20.0,
            "so2": 5.0,
            "co": 1.0
        }
        return defaults.get(parameter, 0.0)
    
    async def _generate_default_forecast(self, forecast_hours: int) -> Dict[str, Any]:
        """Generate default forecast when no data is available"""
        forecast_data = []
        
        for hour in range(forecast_hours):
            forecast_time = datetime.utcnow() + timedelta(hours=hour)
            
            forecast_point = ForecastDataPoint(
                timestamp=forecast_time,
                pm25=self._get_default_value("pm25"),
                o3=self._get_default_value("o3"),
                no2=self._get_default_value("no2"),
                aqi=50
            )
            
            forecast_data.append(forecast_point)
        
        return {
            "forecast_data": forecast_data,
            "model_info": {"status": "default", "message": "Using default values"},
            "data_sources": []
        }
    
    async def get_current_conditions(
        self,
        latitude: float,
        longitude: float
    ) -> Dict[str, Any]:
        """Get current air quality conditions for a location"""
        try:
            # This would typically query the database for the latest readings
            # For now, return mock current conditions
            
            current_conditions = {
                "pm25": self._get_default_value("pm25"),
                "o3": self._get_default_value("o3"),
                "no2": self._get_default_value("no2"),
                "aqi": 50,
                "quality_flag": "Good",
                "data_source": "forecast"
            }
            
            return current_conditions
            
        except Exception as e:
            logger.error(f"Error getting current conditions: {str(e)}")
            return {
                "pm25": self._get_default_value("pm25"),
                "o3": self._get_default_value("o3"),
                "no2": self._get_default_value("no2"),
                "aqi": 50,
                "quality_flag": "Unknown",
                "data_source": "default"
            }
    
    async def get_available_models(self) -> List[Dict[str, Any]]:
        """Get information about available forecast models"""
        try:
            models = []
            
            for param, model in self.models.items():
                models.append({
                    "parameter": param,
                    "model_type": type(model).__name__,
                    "is_loaded": True,
                    "last_updated": datetime.utcnow().isoformat()
                })
            
            # Add default models for parameters without loaded models
            all_parameters = ["pm25", "o3", "no2", "aqi"]
            loaded_parameters = list(self.models.keys())
            
            for param in all_parameters:
                if param not in loaded_parameters:
                    models.append({
                        "parameter": param,
                        "model_type": "default",
                        "is_loaded": False,
                        "last_updated": None
                    })
            
            return models
            
        except Exception as e:
            logger.error(f"Error getting available models: {str(e)}")
            return []
    
    async def _get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        return {
            "models_loaded": len(self.models),
            "available_parameters": list(self.models.keys()),
            "model_path": self.model_path,
            "last_updated": datetime.utcnow().isoformat()
        }
