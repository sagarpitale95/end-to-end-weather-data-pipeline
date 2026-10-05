-- ============================================
-- Weather Data Analysis
-- ============================================


-- 1. Total observations

SELECT
    COUNT(*) AS total_observations
FROM fact_weather;


-- 2. Observations by city

SELECT
    city,
    COUNT(*) AS observation_count
FROM fact_weather
GROUP BY city
ORDER BY observation_count DESC;


-- 3. Average temperature by city

SELECT
    city,
    ROUND(AVG(temperature_celsius), 2)
        AS average_temperature_celsius
FROM fact_weather
GROUP BY city
ORDER BY average_temperature_celsius DESC;


-- 4. Average humidity by city

SELECT
    city,
    ROUND(AVG(humidity_percent), 2)
        AS average_humidity_percent
FROM fact_weather
GROUP BY city
ORDER BY average_humidity_percent DESC;


-- 5. Maximum wind speed by city

SELECT
    city,
    ROUND(MAX(wind_speed_kmh), 2)
        AS maximum_wind_speed_kmh
FROM fact_weather
GROUP BY city
ORDER BY maximum_wind_speed_kmh DESC;