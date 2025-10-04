import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import json

from app.core.config import settings
from app.models.air_quality import UserAlert, AirQualityReading
from app.schemas import AlertRequest, AlertResponse, AlertSubscription, AirQualityParameter

logger = logging.getLogger(__name__)

class NotificationService:
    """Service for managing alerts and notifications"""
    
    def __init__(self):
        self.web_push_enabled = bool(settings.WEB_PUSH_VAPID_PUBLIC_KEY)
        self.email_enabled = False  # Would be configured with SendGrid
        self.sms_enabled = False    # Would be configured with Twilio
        
    async def initialize(self):
        """Initialize notification service"""
        try:
            if self.web_push_enabled:
                logger.info("Web push notifications enabled")
            else:
                logger.warning("Web push notifications not configured")
                
            logger.info("Notification service initialized")
        except Exception as e:
            logger.error(f"Error initializing notification service: {str(e)}")
    
    async def get_active_alerts(
        self,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        radius: Optional[float] = None,
        hours: int = 24
    ) -> List[AlertResponse]:
        """Get active air quality alerts"""
        try:
            alerts = []
            
            # Calculate time range
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(hours=hours)
            
            # This would typically query the database for active alerts
            # For now, generate mock alerts
            
            mock_alerts = self._generate_mock_alerts(
                latitude, longitude, radius, start_time, end_time
            )
            
            return mock_alerts
            
        except Exception as e:
            logger.error(f"Error getting active alerts: {str(e)}")
            return []
    
    def _generate_mock_alerts(
        self,
        latitude: Optional[float],
        longitude: Optional[float],
        radius: Optional[float],
        start_time: datetime,
        end_time: datetime
    ) -> List[AlertResponse]:
        """Generate mock alerts for testing"""
        alerts = []
        
        # Generate a few mock alerts
        alert_locations = [
            {"lat": 40.7128, "lon": -74.0060, "city": "New York"},
            {"lat": 34.0522, "lon": -118.2437, "city": "Los Angeles"},
            {"lat": 41.8781, "lon": -87.6298, "city": "Chicago"}
        ]
        
        for i, location in enumerate(alert_locations):
            if latitude and longitude and radius:
                # Check if location is within radius
                distance = self._calculate_distance(
                    latitude, longitude, location["lat"], location["lon"]
                )
                if distance > radius:
                    continue
            
            alert = AlertResponse(
                id=f"alert_{i}",
                location={"latitude": location["lat"], "longitude": location["lon"]},
                parameter=AirQualityParameter.PM25,
                threshold=35.4,
                current_value=45.2,
                severity="Unhealthy for Sensitive Groups",
                message=f"PM2.5 levels in {location['city']} are elevated",
                timestamp=datetime.utcnow(),
                expires_at=datetime.utcnow() + timedelta(hours=6)
            )
            
            alerts.append(alert)
        
        return alerts
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points in kilometers"""
        from math import radians, cos, sin, asin, sqrt
        
        # Convert decimal degrees to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        
        # Radius of earth in kilometers
        r = 6371
        return c * r
    
    async def create_subscription(
        self,
        subscription: AlertSubscription,
        db: Session
    ) -> UserAlert:
        """Create a new alert subscription"""
        try:
            # Create new subscription
            user_alert = UserAlert(
                user_id=subscription.user_id,
                latitude=subscription.latitude,
                longitude=subscription.longitude,
                pm25_threshold=subscription.pm25_threshold,
                o3_threshold=subscription.o3_threshold,
                no2_threshold=subscription.no2_threshold,
                aqi_threshold=subscription.aqi_threshold,
                web_push_enabled=subscription.web_push_enabled,
                email_enabled=subscription.email_enabled,
                sms_enabled=subscription.sms_enabled,
                is_active=True
            )
            
            db.add(user_alert)
            db.commit()
            db.refresh(user_alert)
            
            logger.info(f"Created alert subscription for user {subscription.user_id}")
            return user_alert
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating subscription: {str(e)}")
            raise
    
    async def cancel_subscription(
        self,
        subscription_id: str,
        db: Session
    ) -> bool:
        """Cancel an alert subscription"""
        try:
            subscription = db.query(UserAlert).filter(
                UserAlert.id == subscription_id
            ).first()
            
            if not subscription:
                return False
            
            subscription.is_active = False
            db.commit()
            
            logger.info(f"Cancelled subscription {subscription_id}")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error cancelling subscription {subscription_id}: {str(e)}")
            return False
    
    async def send_test_alert(self, request: AlertRequest) -> str:
        """Send a test alert notification"""
        try:
            # Generate test alert
            alert = AlertResponse(
                id="test_alert",
                location={"latitude": request.latitude, "longitude": request.longitude},
                parameter=request.parameter,
                threshold=request.threshold,
                current_value=request.threshold + 10,  # Mock current value
                severity=self._get_severity_level(request.parameter, request.threshold),
                message=request.message or f"{request.parameter.value} threshold exceeded",
                timestamp=datetime.utcnow(),
                expires_at=datetime.utcnow() + timedelta(hours=6)
            )
            
            # Send notifications based on user preferences
            notification_id = f"test_{datetime.utcnow().timestamp()}"
            
            if self.web_push_enabled:
                await self._send_web_push_notification(alert, request.user_id)
            
            if self.email_enabled:
                await self._send_email_notification(alert, request.user_id)
            
            if self.sms_enabled:
                await self._send_sms_notification(alert, request.user_id)
            
            logger.info(f"Sent test alert {notification_id}")
            return notification_id
            
        except Exception as e:
            logger.error(f"Error sending test alert: {str(e)}")
            raise
    
    def _get_severity_level(self, parameter: AirQualityParameter, threshold: float) -> str:
        """Get severity level based on parameter and threshold"""
        if parameter == AirQualityParameter.PM25:
            if threshold <= 12.0:
                return "Good"
            elif threshold <= 35.4:
                return "Moderate"
            elif threshold <= 55.4:
                return "Unhealthy for Sensitive Groups"
            else:
                return "Unhealthy"
        elif parameter == AirQualityParameter.O3:
            if threshold <= 0.054:
                return "Good"
            elif threshold <= 0.070:
                return "Moderate"
            elif threshold <= 0.085:
                return "Unhealthy for Sensitive Groups"
            else:
                return "Unhealthy"
        else:
            return "Moderate"
    
    async def _send_web_push_notification(self, alert: AlertResponse, user_id: Optional[str]):
        """Send web push notification"""
        try:
            if not self.web_push_enabled:
                return
            
            # This would integrate with a web push service
            # For now, just log the notification
            
            notification_data = {
                "title": "Air Quality Alert",
                "body": alert.message,
                "icon": "/icons/air-quality.png",
                "badge": "/icons/badge.png",
                "data": {
                    "alert_id": alert.id,
                    "parameter": alert.parameter.value,
                    "severity": alert.severity,
                    "location": alert.location
                }
            }
            
            logger.info(f"Web push notification sent: {notification_data}")
            
        except Exception as e:
            logger.error(f"Error sending web push notification: {str(e)}")
    
    async def _send_email_notification(self, alert: AlertResponse, user_id: Optional[str]):
        """Send email notification"""
        try:
            if not self.email_enabled:
                return
            
            # This would integrate with SendGrid or similar service
            logger.info(f"Email notification sent for alert {alert.id}")
            
        except Exception as e:
            logger.error(f"Error sending email notification: {str(e)}")
    
    async def _send_sms_notification(self, alert: AlertResponse, user_id: Optional[str]):
        """Send SMS notification"""
        try:
            if not self.sms_enabled:
                return
            
            # This would integrate with Twilio or similar service
            logger.info(f"SMS notification sent for alert {alert.id}")
            
        except Exception as e:
            logger.error(f"Error sending SMS notification: {str(e)}")
    
    async def check_thresholds_and_send_alerts(self, db: Session):
        """Check all active subscriptions and send alerts if thresholds are exceeded"""
        try:
            # Get all active subscriptions
            subscriptions = db.query(UserAlert).filter(
                UserAlert.is_active == True
            ).all()
            
            alerts_sent = 0
            
            for subscription in subscriptions:
                try:
                    # Get current air quality data for the location
                    current_data = await self._get_current_air_quality(
                        subscription.latitude, subscription.longitude
                    )
                    
                    # Check thresholds
                    alert_triggered = False
                    alert_message = ""
                    
                    if subscription.pm25_threshold and current_data.get("pm25", 0) > subscription.pm25_threshold:
                        alert_triggered = True
                        alert_message += f"PM2.5: {current_data['pm25']:.1f} μg/m³ (threshold: {subscription.pm25_threshold:.1f}) "
                    
                    if subscription.o3_threshold and current_data.get("o3", 0) > subscription.o3_threshold:
                        alert_triggered = True
                        alert_message += f"O3: {current_data['o3']:.1f} ppb (threshold: {subscription.o3_threshold:.1f}) "
                    
                    if subscription.no2_threshold and current_data.get("no2", 0) > subscription.no2_threshold:
                        alert_triggered = True
                        alert_message += f"NO2: {current_data['no2']:.1f} ppb (threshold: {subscription.no2_threshold:.1f}) "
                    
                    if subscription.aqi_threshold and current_data.get("aqi", 0) > subscription.aqi_threshold:
                        alert_triggered = True
                        alert_message += f"AQI: {current_data['aqi']} (threshold: {subscription.aqi_threshold}) "
                    
                    if alert_triggered:
                        # Send alert
                        await self._send_subscription_alert(subscription, alert_message, current_data)
                        alerts_sent += 1
                        
                except Exception as e:
                    logger.error(f"Error checking subscription {subscription.id}: {str(e)}")
                    continue
            
            logger.info(f"Checked {len(subscriptions)} subscriptions, sent {alerts_sent} alerts")
            return {"subscriptions_checked": len(subscriptions), "alerts_sent": alerts_sent}
            
        except Exception as e:
            logger.error(f"Error checking thresholds: {str(e)}")
            return {"error": str(e)}
    
    async def _get_current_air_quality(self, latitude: float, longitude: float) -> Dict[str, float]:
        """Get current air quality data for a location"""
        # This would typically query the database or call the forecasting service
        # For now, return mock data
        return {
            "pm25": 25.0,
            "o3": 45.0,
            "no2": 15.0,
            "aqi": 75
        }
    
    async def _send_subscription_alert(
        self,
        subscription: UserAlert,
        message: str,
        current_data: Dict[str, float]
    ):
        """Send alert for a subscription"""
        try:
            alert = AlertResponse(
                id=f"sub_{subscription.id}_{datetime.utcnow().timestamp()}",
                location={"latitude": subscription.latitude, "longitude": subscription.longitude},
                parameter=AirQualityParameter.AQI,
                threshold=subscription.aqi_threshold or 100,
                current_value=current_data.get("aqi", 0),
                severity="Alert",
                message=message,
                timestamp=datetime.utcnow(),
                expires_at=datetime.utcnow() + timedelta(hours=6)
            )
            
            if subscription.web_push_enabled:
                await self._send_web_push_notification(alert, subscription.user_id)
            
            if subscription.email_enabled:
                await self._send_email_notification(alert, subscription.user_id)
            
            if subscription.sms_enabled:
                await self._send_sms_notification(alert, subscription.user_id)
            
            logger.info(f"Sent subscription alert for user {subscription.user_id}")
            
        except Exception as e:
            logger.error(f"Error sending subscription alert: {str(e)}")
