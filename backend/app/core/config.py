from pydantic_settings import BaseSettings
from typing import List, Dict
import os

class Settings(BaseSettings):
    """Application settings for NASA TEMPO Air Quality Monitoring"""
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "NASA TEMPO Air Quality Monitor"
    VERSION: str = "1.0.0"
    
    # NASA TEMPO Coverage Area (North America)
    # TEMPO monitors from Atlantic to Pacific, Yucatan to Canadian oil sands
    TEMPO_BOUNDS: Dict = {
        "north": 55.0,   # Northern Canada
        "south": 18.0,   # Yucatan Peninsula
        "east": -65.0,   # Atlantic coast
        "west": -130.0   # Pacific coast
    }
    
    # NASA Earthdata Credentials
    # Sign up at: https://urs.earthdata.nasa.gov/
    NASA_EARTHDATA_USERNAME: str = os.getenv("NASA_EARTHDATA_USERNAME", "")
    NASA_EARTHDATA_PASSWORD: str = os.getenv("NASA_EARTHDATA_PASSWORD", "")
    
    # NASA ASDC (Atmospheric Science Data Center) URLs
    ASDC_BASE_URL: str = "https://asdc.larc.nasa.gov/data/TEMPO"
    TEMPO_NO2_PRODUCT: str = "TEMPO_NO2_L2_V03"
    TEMPO_O3_PRODUCT: str = "TEMPO_O3TOT_L2_V03"
    TEMPO_HCHO_PRODUCT: str = "TEMPO_HCHO_L2_V03"
    
    # OpenAQ API for ground station data (free, no key required)
    OPENAQ_API_URL: str = "https://api.openaq.org/v2"
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["http://localhost:3000", "http://localhost:8000", "*"]
    
    # Data refresh interval (minutes)
    DATA_REFRESH_INTERVAL: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
