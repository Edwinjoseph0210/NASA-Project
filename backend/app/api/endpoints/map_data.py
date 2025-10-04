from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import logging

from app.core.database import get_db
from app.services.map_service import MapService
from app.schemas.map import MapDataRequest, MapDataResponse

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/map", response_model=MapDataResponse)
async def get_map_data(
    request: MapDataRequest,
    db: Session = Depends(get_db)
):
    """
    Get gridded air quality data for map visualization.
    
    Returns interpolated air quality data across a geographic region
    for heatmap visualization.
    """
    try:
        map_service = MapService()
        
        map_data = await map_service.get_gridded_data(
            bounds=request.bounds,
            resolution=request.resolution,
            parameter=request.parameter,
            timestamp=request.timestamp
        )
        
        return MapDataResponse(
            bounds=request.bounds,
            resolution=request.resolution,
            parameter=request.parameter,
            timestamp=request.timestamp or datetime.utcnow(),
            data=map_data,
            generated_at=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Error generating map data: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate map data")

@router.get("/map/heatmap")
async def get_heatmap_data(
    north: float = Query(..., description="Northern boundary"),
    south: float = Query(..., description="Southern boundary"),
    east: float = Query(..., description="Eastern boundary"),
    west: float = Query(..., description="Western boundary"),
    parameter: str = Query("aqi", description="Air quality parameter"),
    resolution: float = Query(0.1, description="Grid resolution in degrees"),
    db: Session = Depends(get_db)
):
    """
    Get heatmap data for a geographic region.
    """
    try:
        bounds = {
            "north": north,
            "south": south,
            "east": east,
            "west": west
        }
        
        map_service = MapService()
        
        heatmap_data = await map_service.get_heatmap_data(
            bounds=bounds,
            parameter=parameter,
            resolution=resolution
        )
        
        return {
            "bounds": bounds,
            "parameter": parameter,
            "resolution": resolution,
            "timestamp": datetime.utcnow(),
            "data": heatmap_data
        }
        
    except Exception as e:
        logger.error(f"Error generating heatmap data: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate heatmap data")

@router.get("/map/tempo-coverage")
async def get_tempo_coverage(
    north: float = Query(..., description="Northern boundary"),
    south: float = Query(..., description="Southern boundary"),
    east: float = Query(..., description="Eastern boundary"),
    west: float = Query(..., description="Western boundary"),
    db: Session = Depends(get_db)
):
    """
    Get NASA TEMPO satellite coverage data for a region.
    """
    try:
        bounds = {
            "north": north,
            "south": south,
            "east": east,
            "west": west
        }
        
        map_service = MapService()
        
        tempo_data = await map_service.get_tempo_coverage(
            bounds=bounds
        )
        
        return {
            "bounds": bounds,
            "timestamp": datetime.utcnow(),
            "tempo_data": tempo_data
        }
        
    except Exception as e:
        logger.error(f"Error getting TEMPO coverage: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get TEMPO coverage")

@router.get("/map/contours")
async def get_contour_data(
    north: float = Query(..., description="Northern boundary"),
    south: float = Query(..., description="Southern boundary"),
    east: float = Query(..., description="Eastern boundary"),
    west: float = Query(..., description="Western boundary"),
    parameter: str = Query("aqi", description="Air quality parameter"),
    levels: List[float] = Query([50, 100, 150, 200], description="Contour levels"),
    db: Session = Depends(get_db)
):
    """
    Get contour data for air quality visualization.
    """
    try:
        bounds = {
            "north": north,
            "south": south,
            "east": east,
            "west": west
        }
        
        map_service = MapService()
        
        contour_data = await map_service.get_contour_data(
            bounds=bounds,
            parameter=parameter,
            levels=levels
        )
        
        return {
            "bounds": bounds,
            "parameter": parameter,
            "levels": levels,
            "timestamp": datetime.utcnow(),
            "contours": contour_data
        }
        
    except Exception as e:
        logger.error(f"Error generating contour data: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate contour data")
