from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
import uvicorn
from datetime import datetime
import logging

from app.core.config import settings
from app.services.tempo_data import TEMPODataService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="NASA TEMPO Air Quality Monitor",
    description="Real-Time Air Quality Monitoring for North America using NASA TEMPO Satellite Data",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Initialize data service
data_service = TEMPODataService()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "NASA TEMPO Air Quality Monitor - Real-Time Pollution Monitoring",
        "region": "North America",
        "coverage": "Atlantic to Pacific, Yucatan Peninsula to Canadian oil sands",
        "satellite": "NASA TEMPO (Tropospheric Emissions: Monitoring Pollution)",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "continent_summary": "/api/summary",
            "all_cities": "/api/cities",
            "city_detail": "/api/cities/{city_id}",
            "historical_data": "/api/cities/{city_id}/history",
            "forecast": "/api/cities/{city_id}/forecast"
        },
        "tempo_info": {
            "instrument": "TEMPO",
            "launch_date": "April 2023",
            "orbit": "Geostationary",
            "resolution": "Hourly during daylight, ~10km spatial",
            "pollutants": ["NO2", "O3", "HCHO", "Aerosols"]
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.get("/api/summary")
async def get_continent_summary():
    """Get overall air quality summary for North America (TEMPO coverage area)"""
    try:
        summary = await data_service.get_continent_summary()
        return summary
    except Exception as e:
        logger.error(f"Error getting continent summary: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get continent summary")

@app.get("/api/cities")
async def get_all_cities():
    """Get all monitored cities in North America"""
    try:
        cities = data_service.get_cities()
        readings = await data_service.get_current_readings()
        return {
            "region": "North America",
            "satellite": "NASA TEMPO",
            "total_cities": len(cities),
            "cities": readings,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting cities: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get cities")

@app.get("/api/cities/{city_id}")
async def get_city_detail(city_id: str):
    """Get current reading for a specific city"""
    try:
        reading = await data_service.get_city_reading(city_id)
        if not reading:
            raise HTTPException(status_code=404, detail="City not found")
        return reading
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting city {city_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get city data")

@app.get("/api/cities/{city_id}/history")
async def get_city_history(
    city_id: str,
    hours: int = Query(24, description="Number of hours of historical data", ge=1, le=168)
):
    """Get historical data for a city"""
    try:
        history = await data_service.get_historical_data(city_id, hours)
        if not history:
            raise HTTPException(status_code=404, detail="City not found")
        return {
            "city_id": city_id,
            "hours": hours,
            "data_points": len(history),
            "data": history
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting history for {city_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get historical data")

@app.get("/api/cities/{city_id}/forecast")
async def get_city_forecast(
    city_id: str,
    hours: int = Query(24, description="Forecast horizon in hours", ge=1, le=72)
):
    """Get forecast for a city"""
    try:
        forecast = await data_service.get_forecast(city_id, hours)
        if not forecast:
            raise HTTPException(status_code=404, detail="City not found")
        return {
            "city_id": city_id,
            "forecast_hours": hours,
            "data_points": len(forecast),
            "forecast": forecast,
            "note": "Forecast based on TEMPO observation patterns"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting forecast for {city_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get forecast")

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting NASA TEMPO Air Quality Monitor API...")
    logger.info(f"Monitoring {len(data_service.get_cities())} major cities across North America")
    logger.info("Coverage: Atlantic to Pacific, Yucatan to Canadian oil sands")
    await data_service.initialize()
    logger.info("API started successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down NASA TEMPO Air Quality Monitor API...")
    await data_service.close()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
