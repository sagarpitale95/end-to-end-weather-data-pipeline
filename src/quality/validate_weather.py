import json
from pathlib import Path


REQUIRED_WEATHER_FIELDS = [
    "temperature_2m",
    "relative_humidity_2m",
    "wind_speed_10m",
    "weather_code"
]


def validate_weather_data(data):
    """
    Validate the basic structure of a weather API response.

    Returns:
        tuple: (is_valid, list_of_errors)
    """

    errors = []

    # Check top-level fields
    required_top_level_fields = [
        "city",
        "latitude",
        "longitude",
        "ingested_at",
        "weather"
    ]

    for field in required_top_level_fields:
        if field not in data:
            errors.append(f"Missing top-level field: {field}")

    # Stop further validation if weather object is missing
    if "weather" not in data:
        return False, errors

    weather = data["weather"]

    # Check current weather section
    if "current" not in weather:
        errors.append("Missing current weather data")
        return False, errors

    current = weather["current"]

    # Check required weather fields
    for field in REQUIRED_WEATHER_FIELDS:
        if field not in current:
            errors.append(f"Missing weather field: {field}")

    # Validate coordinates
    if not isinstance(data.get("latitude"), (int, float)):
        errors.append("Latitude must be numeric")

    if not isinstance(data.get("longitude"), (int, float)):
        errors.append("Longitude must be numeric")

    # Validate city
    if not isinstance(data.get("city"), str) or not data.get("city"):
        errors.append("City must be a non-empty string")

    return len(errors) == 0, errors


def validate_file(file_path):
    """Validate a raw weather JSON file."""

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return validate_weather_data(data)


if __name__ == "__main__":

    project_root = Path(__file__).resolve().parents[2]
    raw_data_dir = project_root / "data" / "raw"

    json_files = list(raw_data_dir.glob("*.json"))

    print(f"Found {len(json_files)} JSON files")

    for file_path in json_files:

        is_valid, errors = validate_file(file_path)

        if is_valid:
            print(f"PASS: {file_path.name}")
        else:
            print(f"FAIL: {file_path.name}")

            for error in errors:
                print(f"  - {error}")