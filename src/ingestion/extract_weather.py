import json
import logging
from datetime import datetime, timezone
from pathlib import Path

import requests


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_FILE = PROJECT_ROOT / "config" / "cities.json"
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

API_URL = "https://api.open-meteo.com/v1/forecast"


# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


def load_cities():
    """Load city configuration from JSON."""
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def fetch_weather(city):
    """Fetch current weather data for a city."""

    params = {
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        "timezone": "UTC"
    }

    response = requests.get(
        API_URL,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    return response.json()


def save_raw_data(city, weather_data):
    """Save API response as a raw JSON file."""

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    ingestion_timestamp = datetime.now(timezone.utc).strftime(
        "%Y%m%dT%H%M%SZ"
    )

    filename = (
        f"{city['city'].lower()}_"
        f"{ingestion_timestamp}.json"
    )

    output_file = RAW_DATA_DIR / filename

    payload = {
        "city": city["city"],
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        "weather": weather_data
    }

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(payload, file, indent=4)

    logger.info("Saved raw data: %s", output_file)


def main():
    """Run the weather ingestion pipeline."""

    logger.info("Starting weather data ingestion")

    cities = load_cities()

    logger.info("Loaded %d cities", len(cities))

    for city in cities:
        logger.info("Fetching weather data for %s", city["city"])

        try:
            weather_data = fetch_weather(city)
            save_raw_data(city, weather_data)

        except requests.RequestException as error:
            logger.error(
                "Failed to fetch data for %s: %s",
                city["city"],
                error
            )

    logger.info("Weather data ingestion completed")


if __name__ == "__main__":
    main()