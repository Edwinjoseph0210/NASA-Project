import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import numpy as np
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.air_quality import AirQualityReading, AirQualityStation, TEMPOData
from app.schemas import AirQualityParameter

logger = logging.getLogger(__name__)

class MapService:
    """Service for generating map data and visualizations"""
    
    def __init__(self):
        self.interpolation_method = "kriging"  # or "idw", "rbf"
        
    async def get_gridded_data(
        self,
        bounds: Dict[str, float],
        resolution: float = 0.1,
        parameter: AirQualityParameter = AirQualityParameter.AQI,
        timestamp: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """Generate gridded air quality data for map visualization"""
        try:
            if timestamp is None:
                timestamp = datetime.utcnow()
            
            # Generate grid points
            grid_points = self._generate_grid_points(bounds, resolution)
            
            # Get station data for interpolation
            station_data = await self._get_station_data_for_interpolation(
                bounds, timestamp, parameter
            )
            
            if not station_data:
                # Return default values if no station data
                return self._generate_default_grid_data(grid_points, parameter)
            
            # Interpolate values at grid points
            interpolated_data = await self._interpolate_values(
                station_data, grid_points, parameter
            )
            
            return interpolated_data
            
        except Exception as e:
            logger.error(f"Error generating gridded data: {str(e)}")
            return self._generate_default_grid_data(
                self._generate_grid_points(bounds, resolution), parameter
            )
    
    def _generate_grid_points(
        self,
        bounds: Dict[str, float],
        resolution: float
    ) -> List[Tuple[float, float]]:
        """Generate grid points within bounds"""
        grid_points = []
        
        lat_start = bounds["south"]
        lat_end = bounds["north"]
        lon_start = bounds["west"]
        lon_end = bounds["east"]
        
        lat_points = np.arange(lat_start, lat_end + resolution, resolution)
        lon_points = np.arange(lon_start, lon_end + resolution, resolution)
        
        for lat in lat_points:
            for lon in lon_points:
                grid_points.append((lat, lon))
        
        return grid_points
    
    async def _get_station_data_for_interpolation(
        self,
        bounds: Dict[str, float],
        timestamp: datetime,
        parameter: AirQualityParameter
    ) -> List[Dict[str, Any]]:
        """Get station data for interpolation"""
        try:
            # This would typically query the database
            # For now, return mock station data
            
            station_data = []
            
            # Generate mock stations within bounds
            num_stations = 20
            for i in range(num_stations):
                lat = np.random.uniform(bounds["south"], bounds["north"])
                lon = np.random.uniform(bounds["west"], bounds["east"])
                
                # Mock air quality values
                value = self._get_mock_value(parameter)
                
                station_data.append({
                    "latitude": lat,
                    "longitude": lon,
                    "value": value,
                    "timestamp": timestamp,
                    "station_id": f"mock_station_{i}"
                })
            
            return station_data
            
        except Exception as e:
            logger.error(f"Error getting station data: {str(e)}")
            return []
    
    def _get_mock_value(self, parameter: AirQualityParameter) -> float:
        """Get mock value for a parameter"""
        mock_values = {
            AirQualityParameter.PM25: np.random.normal(15, 5),
            AirQualityParameter.O3: np.random.normal(40, 10),
            AirQualityParameter.NO2: np.random.normal(20, 5),
            AirQualityParameter.AQI: np.random.randint(30, 80)
        }
        return mock_values.get(parameter, 50.0)
    
    async def _interpolate_values(
        self,
        station_data: List[Dict[str, Any]],
        grid_points: List[Tuple[float, float]],
        parameter: AirQualityParameter
    ) -> List[Dict[str, Any]]:
        """Interpolate values at grid points"""
        try:
            interpolated_data = []
            
            # Extract coordinates and values
            station_coords = np.array([(s["latitude"], s["longitude"]) for s in station_data])
            station_values = np.array([s["value"] for s in station_data])
            
            # Use inverse distance weighting for interpolation
            for lat, lon in grid_points:
                interpolated_value = self._inverse_distance_weighting(
                    lat, lon, station_coords, station_values
                )
                
                interpolated_data.append({
                    "latitude": lat,
                    "longitude": lon,
                    "value": interpolated_value,
                    "confidence": 0.8  # Mock confidence
                })
            
            return interpolated_data
            
        except Exception as e:
            logger.error(f"Error interpolating values: {str(e)}")
            return []
    
    def _inverse_distance_weighting(
        self,
        target_lat: float,
        target_lon: float,
        station_coords: np.ndarray,
        station_values: np.ndarray,
        power: float = 2.0
    ) -> float:
        """Inverse distance weighting interpolation"""
        try:
            # Calculate distances
            distances = np.sqrt(
                (station_coords[:, 0] - target_lat) ** 2 +
                (station_coords[:, 1] - target_lon) ** 2
            )
            
            # Avoid division by zero
            distances = np.maximum(distances, 1e-10)
            
            # Calculate weights
            weights = 1.0 / (distances ** power)
            
            # Calculate weighted average
            weighted_value = np.sum(weights * station_values) / np.sum(weights)
            
            return float(weighted_value)
            
        except Exception as e:
            logger.error(f"Error in IDW interpolation: {str(e)}")
            return 50.0
    
    def _generate_default_grid_data(
        self,
        grid_points: List[Tuple[float, float]],
        parameter: AirQualityParameter
    ) -> List[Dict[str, Any]]:
        """Generate default grid data when no station data is available"""
        default_data = []
        
        for lat, lon in grid_points:
            default_data.append({
                "latitude": lat,
                "longitude": lon,
                "value": self._get_mock_value(parameter),
                "confidence": 0.5
            })
        
        return default_data
    
    async def get_heatmap_data(
        self,
        bounds: Dict[str, float],
        parameter: AirQualityParameter = AirQualityParameter.AQI,
        resolution: float = 0.1
    ) -> Dict[str, Any]:
        """Get heatmap data for visualization"""
        try:
            # Get gridded data
            grid_data = await self.get_gridded_data(
                bounds=bounds,
                resolution=resolution,
                parameter=parameter
            )
            
            # Format for heatmap visualization
            heatmap_data = {
                "type": "heatmap",
                "parameter": parameter.value,
                "bounds": bounds,
                "resolution": resolution,
                "data": grid_data,
                "color_scale": self._get_color_scale(parameter),
                "timestamp": datetime.utcnow()
            }
            
            return heatmap_data
            
        except Exception as e:
            logger.error(f"Error generating heatmap data: {str(e)}")
            return {"error": str(e)}
    
    def _get_color_scale(self, parameter: AirQualityParameter) -> Dict[str, Any]:
        """Get color scale for parameter visualization"""
        color_scales = {
            AirQualityParameter.AQI: {
                "type": "discrete",
                "colors": ["#00e400", "#ffff00", "#ff7e00", "#ff0000", "#8f3f97", "#7e0023"],
                "thresholds": [50, 100, 150, 200, 300, 500]
            },
            AirQualityParameter.PM25: {
                "type": "continuous",
                "colors": ["#00e400", "#ffff00", "#ff7e00", "#ff0000"],
                "range": [0, 50]
            },
            AirQualityParameter.O3: {
                "type": "continuous",
                "colors": ["#00e400", "#ffff00", "#ff7e00", "#ff0000"],
                "range": [0, 200]
            },
            AirQualityParameter.NO2: {
                "type": "continuous",
                "colors": ["#00e400", "#ffff00", "#ff7e00", "#ff0000"],
                "range": [0, 100]
            }
        }
        
        return color_scales.get(parameter, color_scales[AirQualityParameter.AQI])
    
    async def get_tempo_coverage(
        self,
        bounds: Dict[str, float]
    ) -> Dict[str, Any]:
        """Get NASA TEMPO satellite coverage data"""
        try:
            # This would typically query TEMPO data from the database
            # For now, return mock TEMPO coverage
            
            tempo_coverage = {
                "bounds": bounds,
                "coverage_points": [],
                "latest_observation": datetime.utcnow(),
                "data_quality": "good"
            }
            
            # Generate mock TEMPO coverage points
            num_points = 50
            for i in range(num_points):
                lat = np.random.uniform(bounds["south"], bounds["north"])
                lon = np.random.uniform(bounds["west"], bounds["east"])
                
                tempo_coverage["coverage_points"].append({
                    "latitude": lat,
                    "longitude": lon,
                    "no2_column": np.random.normal(0.3, 0.1),
                    "o3_column": np.random.normal(300, 50),
                    "cloud_fraction": np.random.uniform(0, 1),
                    "quality_flag": "good"
                })
            
            return tempo_coverage
            
        except Exception as e:
            logger.error(f"Error getting TEMPO coverage: {str(e)}")
            return {"error": str(e)}
    
    async def get_contour_data(
        self,
        bounds: Dict[str, float],
        parameter: AirQualityParameter = AirQualityParameter.AQI,
        levels: List[float] = [50, 100, 150, 200]
    ) -> Dict[str, Any]:
        """Get contour data for air quality visualization"""
        try:
            # Get gridded data
            grid_data = await self.get_gridded_data(
                bounds=bounds,
                resolution=0.05,  # Higher resolution for contours
                parameter=parameter
            )
            
            # Generate contours
            contours = self._generate_contours(grid_data, levels)
            
            return {
                "bounds": bounds,
                "parameter": parameter.value,
                "levels": levels,
                "contours": contours,
                "timestamp": datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"Error generating contour data: {str(e)}")
            return {"error": str(e)}
    
    def _generate_contours(
        self,
        grid_data: List[Dict[str, Any]],
        levels: List[float]
    ) -> List[Dict[str, Any]]:
        """Generate contour lines from grid data"""
        try:
            # This is a simplified contour generation
            # In practice, you would use scipy.interpolate or similar
            
            contours = []
            
            for level in levels:
                contour_points = []
                
                # Find points near the contour level
                for point in grid_data:
                    if abs(point["value"] - level) < 5:  # Within 5 units of level
                        contour_points.append({
                            "latitude": point["latitude"],
                            "longitude": point["longitude"]
                        })
                
                contours.append({
                    "level": level,
                    "points": contour_points,
                    "color": self._get_contour_color(level)
                })
            
            return contours
            
        except Exception as e:
            logger.error(f"Error generating contours: {str(e)}")
            return []
    
    def _get_contour_color(self, level: float) -> str:
        """Get color for contour level"""
        if level <= 50:
            return "#00e400"
        elif level <= 100:
            return "#ffff00"
        elif level <= 150:
            return "#ff7e00"
        elif level <= 200:
            return "#ff0000"
        elif level <= 300:
            return "#8f3f97"
        else:
            return "#7e0023"
