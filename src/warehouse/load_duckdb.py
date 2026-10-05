import logging
from pathlib import Path

import duckdb


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PARQUET_FILE = PROJECT_ROOT / "data" / "processed" / "weather.parquet"
WAREHOUSE_DIR = PROJECT_ROOT / "data" / "warehouse"
DATABASE_FILE = WAREHOUSE_DIR / "weather.duckdb"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


def create_warehouse():
    """Create or refresh the DuckDB weather warehouse."""

    WAREHOUSE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    logger.info(
        "Connecting to DuckDB: %s",
        DATABASE_FILE
    )

    connection = duckdb.connect(str(DATABASE_FILE))

    logger.info("Creating staging table")

    connection.execute(
        """
        CREATE OR REPLACE TABLE staging_weather AS
        SELECT
            city,
            latitude,
            longitude,
            CAST(ingested_at AS TIMESTAMP) AS ingested_at,
            CAST(weather_time AS TIMESTAMP) AS weather_time,
            temperature_celsius,
            humidity_percent,
            wind_speed_kmh,
            weather_code
        FROM read_parquet(?)
        """,
        [str(PARQUET_FILE)]
    )

    logger.info("Creating fact_weather table")

    connection.execute(
        """
        CREATE OR REPLACE TABLE fact_weather AS
        SELECT *
        FROM (
            SELECT
                *,
                ROW_NUMBER() OVER (
                    PARTITION BY city, weather_time
                    ORDER BY ingested_at DESC
                ) AS row_number
            FROM staging_weather
        )
        WHERE row_number = 1
        """
    )

    connection.execute(
        """
        ALTER TABLE fact_weather
        DROP COLUMN row_number
        """
    )

    row_count = connection.execute(
        "SELECT COUNT(*) FROM fact_weather"
    ).fetchone()[0]

    logger.info(
        "Warehouse contains %d unique weather observations",
        row_count
    )

    connection.close()

    logger.info(
        "DuckDB warehouse loading completed"
    )


if __name__ == "__main__":
    create_warehouse()