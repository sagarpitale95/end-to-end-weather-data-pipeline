from src.quality.validate_weather import validate_weather_data


def valid_weather_data():
    """Return a valid weather record for testing."""

    return {
        "city": "Dublin",
        "latitude": 53.3498,
        "longitude": -6.2603,
        "ingested_at": "2026-10-05T20:00:00+00:00",
        "weather": {
            "current": {
                "time": "2026-10-05T20:00",
                "temperature_2m": 15.5,
                "relative_humidity_2m": 80,
                "wind_speed_10m": 12.5,
                "weather_code": 3
            }
        }
    }


def test_valid_weather_data():
    """Valid weather data should pass validation."""

    data = valid_weather_data()

    is_valid, errors = validate_weather_data(data)

    assert is_valid is True
    assert errors == []


def test_missing_weather_field():
    """Missing weather fields should fail validation."""

    data = valid_weather_data()

    del data["weather"]["current"]["temperature_2m"]

    is_valid, errors = validate_weather_data(data)

    assert is_valid is False
    assert "Missing weather field: temperature_2m" in errors


def test_invalid_latitude():
    """Latitude must be numeric."""

    data = valid_weather_data()

    data["latitude"] = "INVALID"

    is_valid, errors = validate_weather_data(data)

    assert is_valid is False
    assert "Latitude must be numeric" in errors


def test_invalid_longitude():
    """Longitude must be numeric."""

    data = valid_weather_data()

    data["longitude"] = "INVALID"

    is_valid, errors = validate_weather_data(data)

    assert is_valid is False
    assert "Longitude must be numeric" in errors