import json
import logging
from pathlib import Path

import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


def load_json_files():
    """Load all raw weather JSON files."""

    json_files = list(RAW_DATA_DIR.glob("*.json"))

    logger.info("Found %d raw JSON files", len(json_files))

    records = []

    for file_path in json_files:

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        records.append(data)

    return records


def transform_weather_data(records):
    """Transform nested JSON into a flat analytical structure."""

    transformed_records = []

    for record in records:

        weather = record["weather"]
        current = weather["current"]

        transformed_records.append(
            {
                "city": record["city"],
                "latitude": record["latitude"],
                "longitude": record["longitude"],
                "ingested_at": record["ingested_at"],
                "weather_time": current["time"],
                "temperature_celsius": current["temperature_2m"],
                "humidity_percent": current["relative_humidity_2m"],
                "wind_speed_kmh": current["wind_speed_10m"],
                "weather_code": current["weather_code"]
            }
        )

    return transformed_records


def save_parquet(records):
    """Save transformed records as a Parquet file."""

    PROCESSED_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    dataframe = pd.DataFrame(records)

    output_file = PROCESSED_DATA_DIR / "weather.parquet"

    dataframe.to_parquet(
        output_file,
        index=False
    )

    logger.info(
        "Saved %d records to %s",
        len(dataframe),
        output_file
    )


def main():
    """Run the JSON to Parquet transformation."""

    logger.info("Starting JSON to Parquet transformation")

    records = load_json_files()

    if not records:
        logger.warning("No raw JSON files found")
        return

    transformed_records = transform_weather_data(records)

    save_parquet(transformed_records)

    logger.info(
        "JSON to Parquet transformation completed"
    )


if __name__ == "__main__":
    main()