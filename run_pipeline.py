import logging
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


PIPELINE_STEPS = [
    (
        "Extract weather data",
        PROJECT_ROOT / "src" / "ingestion" / "extract_weather.py"
    ),
    (
        "Validate weather data",
        PROJECT_ROOT / "src" / "quality" / "validate_weather.py"
    ),
    (
        "Transform JSON to Parquet",
        PROJECT_ROOT / "src" / "transformation" / "json_to_parquet.py"
    ),
    (
        "Load DuckDB warehouse",
        PROJECT_ROOT / "src" / "warehouse" / "load_duckdb.py"
    ),
]


def run_step(step_name, script_path):
    """Run one pipeline step."""

    logger.info("=" * 60)
    logger.info("STARTING: %s", step_name)
    logger.info("=" * 60)

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=PROJECT_ROOT
    )

    if result.returncode != 0:
        logger.error(
            "FAILED: %s",
            step_name
        )
        return False

    logger.info(
        "COMPLETED: %s",
        step_name
    )

    return True


def main():
    """Run the complete weather data pipeline."""

    logger.info("=" * 60)
    logger.info("WEATHER DATA ENGINEERING PIPELINE")
    logger.info("=" * 60)

    for step_name, script_path in PIPELINE_STEPS:

        success = run_step(
            step_name,
            script_path
        )

        if not success:

            logger.error(
                "Pipeline stopped because '%s' failed.",
                step_name
            )

            sys.exit(1)

    logger.info("=" * 60)
    logger.info("PIPELINE COMPLETED SUCCESSFULLY")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()