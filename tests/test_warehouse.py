import duckdb
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATABASE_FILE = (
    PROJECT_ROOT
    / "data"
    / "warehouse"
    / "weather.duckdb"
)


def test_weather_business_key_is_unique():
    """Ensure city + weather_time contains no duplicates."""

    connection = duckdb.connect(str(DATABASE_FILE))

    duplicate_count = connection.execute(
        """
        SELECT COUNT(*)
        FROM (
            SELECT
                city,
                weather_time
            FROM fact_weather
            GROUP BY city, weather_time
            HAVING COUNT(*) > 1
        )
        """
    ).fetchone()[0]

    connection.close()

    assert duplicate_count == 0