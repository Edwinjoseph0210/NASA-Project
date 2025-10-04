-- Initialize AirAware Database
-- This script sets up the database schema and initial data

-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;

-- Create database schema
CREATE SCHEMA IF NOT EXISTS airaware;

-- Set search path
SET search_path TO airaware, public;

-- Create tables (these will be created by SQLAlchemy models)
-- This file is mainly for initial setup and any custom database configurations

-- Create indexes for better performance
-- These will be created after the tables are created by the application

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE airaware TO postgres;
GRANT ALL PRIVILEGES ON SCHEMA airaware TO postgres;

-- Create a function to calculate distance between two points
CREATE OR REPLACE FUNCTION calculate_distance(
    lat1 DOUBLE PRECISION,
    lon1 DOUBLE PRECISION,
    lat2 DOUBLE PRECISION,
    lon2 DOUBLE PRECISION
) RETURNS DOUBLE PRECISION AS $$
BEGIN
    RETURN ST_Distance(
        ST_GeogFromText('POINT(' || lon1 || ' ' || lat1 || ')'),
        ST_GeogFromText('POINT(' || lon2 || ' ' || lat2 || ')')
    ) / 1000; -- Return distance in kilometers
END;
$$ LANGUAGE plpgsql;

-- Create a function to get nearby stations
CREATE OR REPLACE FUNCTION get_nearby_stations(
    target_lat DOUBLE PRECISION,
    target_lon DOUBLE PRECISION,
    radius_km DOUBLE PRECISION DEFAULT 50.0
) RETURNS TABLE (
    station_id VARCHAR,
    name VARCHAR,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    distance_km DOUBLE PRECISION
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        s.station_id,
        s.name,
        s.latitude,
        s.longitude,
        calculate_distance(target_lat, target_lon, s.latitude, s.longitude) as distance_km
    FROM airaware.air_quality_stations s
    WHERE s.is_active = true
    AND calculate_distance(target_lat, target_lon, s.latitude, s.longitude) <= radius_km
    ORDER BY distance_km;
END;
$$ LANGUAGE plpgsql;

-- Create a function to get latest readings for a station
CREATE OR REPLACE FUNCTION get_latest_readings(
    station_id_param VARCHAR,
    hours_back INTEGER DEFAULT 24
) RETURNS TABLE (
    timestamp TIMESTAMP,
    pm25 DOUBLE PRECISION,
    o3 DOUBLE PRECISION,
    no2 DOUBLE PRECISION,
    overall_aqi INTEGER,
    quality_flag VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        r.timestamp,
        r.pm25,
        r.o3,
        r.no2,
        r.overall_aqi,
        r.quality_flag
    FROM airaware.air_quality_readings r
    JOIN airaware.air_quality_stations s ON r.station_id = s.id
    WHERE s.station_id = station_id_param
    AND r.timestamp >= NOW() - INTERVAL '1 hour' * hours_back
    ORDER BY r.timestamp DESC;
END;
$$ LANGUAGE plpgsql;

-- Create a view for active alerts
CREATE OR REPLACE VIEW active_alerts AS
SELECT 
    a.id,
    a.location,
    a.parameter,
    a.threshold,
    a.current_value,
    a.severity,
    a.message,
    a.timestamp,
    a.expires_at
FROM airaware.user_alerts ua
JOIN airaware.air_quality_readings r ON (
    calculate_distance(
        ua.latitude, ua.longitude,
        ST_Y(r.location), ST_X(r.location)
    ) <= 10.0 -- Within 10km
)
WHERE ua.is_active = true
AND (
    (ua.pm25_threshold IS NOT NULL AND r.pm25 > ua.pm25_threshold) OR
    (ua.o3_threshold IS NOT NULL AND r.o3 > ua.o3_threshold) OR
    (ua.no2_threshold IS NOT NULL AND r.no2 > ua.no2_threshold) OR
    (ua.aqi_threshold IS NOT NULL AND r.overall_aqi > ua.aqi_threshold)
)
AND r.timestamp >= NOW() - INTERVAL '1 hour';

-- Create indexes for better performance (will be created after tables exist)
-- These are commented out as they will be created by the application

-- CREATE INDEX CONCURRENTLY idx_air_quality_stations_location 
-- ON airaware.air_quality_stations USING GIST (location);

-- CREATE INDEX CONCURRENTLY idx_air_quality_readings_timestamp 
-- ON airaware.air_quality_readings (timestamp);

-- CREATE INDEX CONCURRENTLY idx_air_quality_readings_station_timestamp 
-- ON airaware.air_quality_readings (station_id, timestamp);

-- CREATE INDEX CONCURRENTLY idx_tempo_data_timestamp 
-- ON airaware.tempo_data (timestamp);

-- CREATE INDEX CONCURRENTLY idx_weather_data_timestamp 
-- ON airaware.weather_data (timestamp);

-- Insert some sample data (optional)
-- This can be used for testing and development

-- Sample monitoring stations
INSERT INTO airaware.air_quality_stations (
    station_id, name, latitude, longitude, state, city, is_active, location
) VALUES 
    ('NYC001', 'New York City - Manhattan', 40.7128, -74.0060, 'NY', 'New York', true, ST_GeogFromText('POINT(-74.0060 40.7128)')),
    ('LAX001', 'Los Angeles - Downtown', 34.0522, -118.2437, 'CA', 'Los Angeles', true, ST_GeogFromText('POINT(-118.2437 34.0522)')),
    ('CHI001', 'Chicago - Loop', 41.8781, -87.6298, 'IL', 'Chicago', true, ST_GeogFromText('POINT(-87.6298 41.8781)')),
    ('HOU001', 'Houston - Downtown', 29.7604, -95.3698, 'TX', 'Houston', true, ST_GeogFromText('POINT(-95.3698 29.7604)')),
    ('PHX001', 'Phoenix - Central', 33.4484, -112.0740, 'AZ', 'Phoenix', true, ST_GeogFromText('POINT(-112.0740 33.4484)'))
ON CONFLICT (station_id) DO NOTHING;

-- Sample air quality readings
INSERT INTO airaware.air_quality_readings (
    station_id, timestamp, pm25, o3, no2, overall_aqi, data_source, quality_flag
) 
SELECT 
    s.id,
    NOW() - INTERVAL '1 hour' * generate_series(0, 23),
    15 + random() * 10, -- PM2.5 between 15-25
    40 + random() * 20, -- O3 between 40-60
    20 + random() * 10, -- NO2 between 20-30
    50 + random() * 30, -- AQI between 50-80
    'airnow',
    'Good'
FROM airaware.air_quality_stations s
WHERE s.station_id IN ('NYC001', 'LAX001', 'CHI001', 'HOU001', 'PHX001')
ON CONFLICT DO NOTHING;

-- Create a sample user alert
INSERT INTO airaware.user_alerts (
    user_id, latitude, longitude, pm25_threshold, o3_threshold, no2_threshold, aqi_threshold,
    web_push_enabled, email_enabled, sms_enabled, is_active
) VALUES (
    'demo-user', 40.7128, -74.0060, 35.4, 0.070, 0.100, 100,
    true, false, false, true
) ON CONFLICT DO NOTHING;

-- Grant permissions to the postgres user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA airaware TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA airaware TO postgres;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA airaware TO postgres;
