-- Initialize AirAware Kerala Database
-- Focused on Kottayam, Kerala region

-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;

-- Create database schema
CREATE SCHEMA IF NOT EXISTS airaware;

-- Set search path
SET search_path TO airaware, public;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE airaware_kerala TO postgres;
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

-- Insert Kerala-specific monitoring stations
INSERT INTO airaware.air_quality_stations (
    station_id, name, latitude, longitude, state, city, is_active, location
) VALUES 
    ('KT001', 'Kottayam - Medical College', 9.5956, 76.5214, 'KL', 'Kottayam', true, ST_GeogFromText('POINT(76.5214 9.5956)')),
    ('KT002', 'Kottayam - Railway Station', 9.5900, 76.5200, 'KL', 'Kottayam', true, ST_GeogFromText('POINT(76.5200 9.5900)')),
    ('KT003', 'Kottayam - Bus Stand', 9.6000, 76.5300, 'KL', 'Kottayam', true, ST_GeogFromText('POINT(76.5300 9.6000)')),
    ('KT004', 'Kottayam - Industrial Area', 9.5800, 76.5100, 'KL', 'Kottayam', true, ST_GeogFromText('POINT(76.5100 9.5800)')),
    ('KT005', 'Kottayam - Residential Area', 9.6100, 76.5400, 'KL', 'Kottayam', true, ST_GeogFromText('POINT(76.5400 9.6100)')),
    ('KT006', 'Ernakulam - Central', 9.9312, 76.2673, 'KL', 'Ernakulam', true, ST_GeogFromText('POINT(76.2673 9.9312)')),
    ('KT007', 'Thrissur - Central', 10.5276, 76.2144, 'KL', 'Thrissur', true, ST_GeogFromText('POINT(76.2144 10.5276)')),
    ('KT008', 'Alappuzha - Central', 9.4981, 76.3388, 'KL', 'Alappuzha', true, ST_GeogFromText('POINT(76.3388 9.4981)'))
ON CONFLICT (station_id) DO NOTHING;

-- Generate sample air quality readings for Kerala stations
-- Kerala typically has good air quality with some seasonal variations
INSERT INTO airaware.air_quality_readings (
    station_id, timestamp, pm25, o3, no2, overall_aqi, data_source, quality_flag
) 
SELECT 
    s.id,
    NOW() - INTERVAL '1 hour' * generate_series(0, 47), -- Last 48 hours
    CASE 
        WHEN EXTRACT(hour FROM NOW() - INTERVAL '1 hour' * generate_series(0, 47)) BETWEEN 6 AND 9 THEN 18 + random() * 8  -- Morning rush
        WHEN EXTRACT(hour FROM NOW() - INTERVAL '1 hour' * generate_series(0, 47)) BETWEEN 17 AND 20 THEN 20 + random() * 10 -- Evening rush
        ELSE 12 + random() * 6 -- Normal hours
    END as pm25,
    CASE 
        WHEN EXTRACT(hour FROM NOW() - INTERVAL '1 hour' * generate_series(0, 47)) BETWEEN 10 AND 16 THEN 45 + random() * 15 -- Daytime O3
        ELSE 25 + random() * 10 -- Night time
    END as o3,
    CASE 
        WHEN EXTRACT(hour FROM NOW() - INTERVAL '1 hour' * generate_series(0, 47)) BETWEEN 6 AND 9 THEN 25 + random() * 10 -- Morning rush
        WHEN EXTRACT(hour FROM NOW() - INTERVAL '1 hour' * generate_series(0, 47)) BETWEEN 17 AND 20 THEN 30 + random() * 15 -- Evening rush
        ELSE 15 + random() * 8 -- Normal hours
    END as no2,
    CASE 
        WHEN EXTRACT(hour FROM NOW() - INTERVAL '1 hour' * generate_series(0, 47)) BETWEEN 6 AND 9 THEN 55 + random() * 15 -- Morning rush
        WHEN EXTRACT(hour FROM NOW() - INTERVAL '1 hour' * generate_series(0, 47)) BETWEEN 17 AND 20 THEN 60 + random() * 20 -- Evening rush
        ELSE 40 + random() * 15 -- Normal hours
    END as aqi,
    'kerala_demo',
    CASE 
        WHEN (CASE 
            WHEN EXTRACT(hour FROM NOW() - INTERVAL '1 hour' * generate_series(0, 47)) BETWEEN 6 AND 9 THEN 55 + random() * 15
            WHEN EXTRACT(hour FROM NOW() - INTERVAL '1 hour' * generate_series(0, 47)) BETWEEN 17 AND 20 THEN 60 + random() * 20
            ELSE 40 + random() * 15
        END) <= 50 THEN 'Good'
        WHEN (CASE 
            WHEN EXTRACT(hour FROM NOW() - INTERVAL '1 hour' * generate_series(0, 47)) BETWEEN 6 AND 9 THEN 55 + random() * 15
            WHEN EXTRACT(hour FROM NOW() - INTERVAL '1 hour' * generate_series(0, 47)) BETWEEN 17 AND 20 THEN 60 + random() * 20
            ELSE 40 + random() * 15
        END) <= 100 THEN 'Moderate'
        ELSE 'Unhealthy for Sensitive Groups'
    END as quality_flag
FROM airaware.air_quality_stations s
WHERE s.station_id LIKE 'KT%'
ON CONFLICT DO NOTHING;

-- Create sample weather data for Kerala
INSERT INTO airaware.weather_data (
    latitude, longitude, timestamp, temperature, humidity, pressure, wind_speed, wind_direction, data_source
) VALUES 
    (9.5956, 76.5214, NOW() - INTERVAL '1 hour', 28.5, 75, 1013.2, 5.2, 180, 'kerala_demo'),
    (9.5900, 76.5200, NOW() - INTERVAL '1 hour', 29.1, 72, 1012.8, 4.8, 175, 'kerala_demo'),
    (9.6000, 76.5300, NOW() - INTERVAL '1 hour', 28.8, 78, 1013.5, 6.1, 185, 'kerala_demo'),
    (9.5800, 76.5100, NOW() - INTERVAL '1 hour', 29.3, 70, 1012.5, 4.5, 170, 'kerala_demo'),
    (9.6100, 76.5400, NOW() - INTERVAL '1 hour', 28.2, 80, 1013.8, 5.8, 190, 'kerala_demo')
ON CONFLICT DO NOTHING;

-- Create sample TEMPO data for Kerala region
INSERT INTO airaware.tempo_data (
    latitude, longitude, timestamp, no2_column, o3_column, quality_flag
) VALUES 
    (9.6, 76.5, NOW() - INTERVAL '2 hours', 0.25, 280, 'good'),
    (9.5, 76.4, NOW() - INTERVAL '2 hours', 0.28, 285, 'good'),
    (9.7, 76.6, NOW() - INTERVAL '2 hours', 0.22, 275, 'good'),
    (9.4, 76.3, NOW() - INTERVAL '2 hours', 0.30, 290, 'moderate'),
    (9.8, 76.7, NOW() - INTERVAL '2 hours', 0.20, 270, 'good')
ON CONFLICT DO NOTHING;

-- Create a sample user alert for Kottayam
INSERT INTO airaware.user_alerts (
    user_id, latitude, longitude, pm25_threshold, o3_threshold, no2_threshold, aqi_threshold,
    web_push_enabled, email_enabled, sms_enabled, is_active
) VALUES (
    'kerala-user', 9.5956, 76.5214, 35.4, 0.070, 0.100, 100,
    true, false, false, true
) ON CONFLICT DO NOTHING;

-- Grant permissions to the postgres user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA airaware TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA airaware TO postgres;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA airaware TO postgres;
