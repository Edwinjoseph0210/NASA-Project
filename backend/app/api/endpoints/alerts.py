from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import logging

from app.core.database import get_db
from app.models.air_quality import UserAlert
from app.services.notifications import NotificationService
from app.schemas.alerts import AlertRequest, AlertResponse, AlertSubscription

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/alerts", response_model=List[AlertResponse])
async def get_alerts(
    lat: Optional[float] = Query(None, description="Latitude for location filtering"),
    lon: Optional[float] = Query(None, description="Longitude for location filtering"),
    radius: Optional[float] = Query(50.0, description="Radius in kilometers"),
    hours: int = Query(24, description="Hours of alerts to retrieve"),
    db: Session = Depends(get_db)
):
    """
    Get active air quality alerts for a region.
    """
    try:
        notification_service = NotificationService()
        
        alerts = await notification_service.get_active_alerts(
            latitude=lat,
            longitude=lon,
            radius=radius,
            hours=hours
        )
        
        return alerts
        
    except Exception as e:
        logger.error(f"Error fetching alerts: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch alerts")

@router.post("/alerts/subscribe")
async def subscribe_to_alerts(
    subscription: AlertSubscription,
    db: Session = Depends(get_db)
):
    """
    Subscribe to air quality alerts for a location.
    """
    try:
        notification_service = NotificationService()
        
        result = await notification_service.create_subscription(
            subscription=subscription,
            db=db
        )
        
        return {
            "message": "Alert subscription created successfully",
            "subscription_id": result.id,
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        logger.error(f"Error creating alert subscription: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create subscription")

@router.delete("/alerts/subscribe/{subscription_id}")
async def unsubscribe_from_alerts(
    subscription_id: str,
    db: Session = Depends(get_db)
):
    """
    Cancel an alert subscription.
    """
    try:
        notification_service = NotificationService()
        
        result = await notification_service.cancel_subscription(
            subscription_id=subscription_id,
            db=db
        )
        
        if not result:
            raise HTTPException(status_code=404, detail="Subscription not found")
        
        return {
            "message": "Alert subscription cancelled successfully",
            "timestamp": datetime.utcnow()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error cancelling subscription {subscription_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to cancel subscription")

@router.get("/alerts/subscribe/{user_id}")
async def get_user_subscriptions(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Get all alert subscriptions for a user.
    """
    try:
        subscriptions = db.query(UserAlert).filter(
            UserAlert.user_id == user_id,
            UserAlert.is_active == True
        ).all()
        
        return {
            "user_id": user_id,
            "subscriptions": [
                {
                    "id": str(sub.id),
                    "latitude": sub.latitude,
                    "longitude": sub.longitude,
                    "pm25_threshold": sub.pm25_threshold,
                    "o3_threshold": sub.o3_threshold,
                    "no2_threshold": sub.no2_threshold,
                    "aqi_threshold": sub.aqi_threshold,
                    "web_push_enabled": sub.web_push_enabled,
                    "email_enabled": sub.email_enabled,
                    "sms_enabled": sub.sms_enabled,
                    "created_at": sub.created_at
                }
                for sub in subscriptions
            ],
            "total_count": len(subscriptions)
        }
        
    except Exception as e:
        logger.error(f"Error fetching subscriptions for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch subscriptions")

@router.post("/alerts/test")
async def test_alert_notification(
    request: AlertRequest,
    db: Session = Depends(get_db)
):
    """
    Send a test alert notification.
    """
    try:
        notification_service = NotificationService()
        
        result = await notification_service.send_test_alert(
            request=request
        )
        
        return {
            "message": "Test alert sent successfully",
            "notification_id": result,
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        logger.error(f"Error sending test alert: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to send test alert")

@router.get("/alerts/thresholds")
async def get_alert_thresholds():
    """
    Get standard air quality alert thresholds.
    """
    return {
        "aqi_thresholds": {
            "good": {"min": 0, "max": 50, "color": "#00e400"},
            "moderate": {"min": 51, "max": 100, "color": "#ffff00"},
            "unhealthy_sensitive": {"min": 101, "max": 150, "color": "#ff7e00"},
            "unhealthy": {"min": 151, "max": 200, "color": "#ff0000"},
            "very_unhealthy": {"min": 201, "max": 300, "color": "#8f3f97"},
            "hazardous": {"min": 301, "max": 500, "color": "#7e0023"}
        },
        "parameter_thresholds": {
            "pm25": {"unhealthy": 35.4, "very_unhealthy": 55.4},
            "o3": {"unhealthy": 0.164, "very_unhealthy": 0.204},
            "no2": {"unhealthy": 0.360, "very_unhealthy": 0.649}
        },
        "timestamp": datetime.utcnow()
    }
