from celery import Celery
from app.core.config import settings

# Create Celery instance
celery_app = Celery(
    "airaware",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.tasks.data_ingestion",
        "app.tasks.forecasting",
        "app.tasks.notifications",
        "app.tasks.maintenance"
    ]
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    result_expires=3600,  # 1 hour
)

# Beat schedule for periodic tasks
celery_app.conf.beat_schedule = {
    "fetch-airnow-data": {
        "task": "app.tasks.data_ingestion.fetch_airnow_data",
        "schedule": 300.0,  # Every 5 minutes
    },
    "fetch-tempo-data": {
        "task": "app.tasks.data_ingestion.fetch_tempo_data",
        "schedule": 3600.0,  # Every hour
    },
    "fetch-weather-data": {
        "task": "app.tasks.data_ingestion.fetch_weather_data",
        "schedule": 1800.0,  # Every 30 minutes
    },
    "generate-forecasts": {
        "task": "app.tasks.forecasting.generate_forecasts",
        "schedule": 1800.0,  # Every 30 minutes
    },
    "check-alert-thresholds": {
        "task": "app.tasks.notifications.check_thresholds_and_send_alerts",
        "schedule": 300.0,  # Every 5 minutes
    },
    "cleanup-old-data": {
        "task": "app.tasks.maintenance.cleanup_old_data",
        "schedule": 86400.0,  # Daily
    },
    "update-model-performance": {
        "task": "app.tasks.forecasting.update_model_performance",
        "schedule": 3600.0,  # Every hour
    },
}

# Task routing
celery_app.conf.task_routes = {
    "app.tasks.data_ingestion.*": {"queue": "data_ingestion"},
    "app.tasks.forecasting.*": {"queue": "forecasting"},
    "app.tasks.notifications.*": {"queue": "notifications"},
    "app.tasks.maintenance.*": {"queue": "maintenance"},
}

# Error handling
@celery_app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")

if __name__ == "__main__":
    celery_app.start()
