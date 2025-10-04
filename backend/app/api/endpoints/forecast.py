from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import logging

from app.core.database import get_db
from app.services.forecasting import ForecastingService
from app.schemas.forecast import ForecastRequest, ForecastResponse

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/forecast", response_model=ForecastResponse)
async def get_forecast(
    request: ForecastRequest,
    db: Session = Depends(get_db)
):
    """
    Get air quality forecast for a specific location.
    
    Returns forecasted air quality parameters for the next 24-72 hours
    at the specified latitude and longitude.
    """
    try:
        forecasting_service = ForecastingService()
        
        forecast_data = await forecasting_service.generate_forecast(
            latitude=request.latitude,
            longitude=request.longitude,
            forecast_hours=request.forecast_hours,
            include_confidence=request.include_confidence
        )
        
        return ForecastResponse(
            location={
                "latitude": request.latitude,
                "longitude": request.longitude
            },
            forecast_hours=request.forecast_hours,
            generated_at=datetime.utcnow(),
            **forecast_data
        )
        
    except Exception as e:
        logger.error(f"Error generating forecast: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate forecast")

@router.get("/forecast/{lat}/{lon}")
async def get_forecast_by_coordinates(
    lat: float,
    lon: float,
    hours: int = Query(24, description="Forecast horizon in hours (max 72)"),
    include_confidence: bool = Query(False, description="Include confidence intervals"),
    db: Session = Depends(get_db)
):
    """
    Get air quality forecast for specific coordinates.
    """
    try:
        if hours > 72:
            raise HTTPException(status_code=400, detail="Forecast horizon cannot exceed 72 hours")
        
        forecasting_service = ForecastingService()
        
        forecast_data = await forecasting_service.generate_forecast(
            latitude=lat,
            longitude=lon,
            forecast_hours=hours,
            include_confidence=include_confidence
        )
        
        return {
            "location": {
                "latitude": lat,
                "longitude": lon
            },
            "forecast_hours": hours,
            "generated_at": datetime.utcnow(),
            **forecast_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating forecast for {lat}, {lon}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate forecast")

@router.get("/forecast/current")
async def get_current_conditions(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    db: Session = Depends(get_db)
):
    """
    Get current air quality conditions for a location.
    """
    try:
        forecasting_service = ForecastingService()
        
        current_data = await forecasting_service.get_current_conditions(
            latitude=lat,
            longitude=lon
        )
        
        return {
            "location": {
                "latitude": lat,
                "longitude": lon
            },
            "timestamp": datetime.utcnow(),
            **current_data
        }
        
    except Exception as e:
        logger.error(f"Error getting current conditions for {lat}, {lon}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get current conditions")

@router.get("/forecast/models")
async def get_forecast_models(db: Session = Depends(get_db)):
    """
    Get information about available forecast models.
    """
    try:
        forecasting_service = ForecastingService()
        
        models = await forecasting_service.get_available_models()
        
        return {
            "models": models,
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        logger.error(f"Error getting forecast models: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get forecast models")
