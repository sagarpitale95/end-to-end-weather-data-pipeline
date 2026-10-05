# End-to-End Weather Data Engineering Pipeline

[![CI](https://github.com/sagarpitale95/end-to-end-weather-data-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/sagarpitale95/end-to-end-weather-data-pipeline/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.x-blue)](https://www.python.org/)
[![DuckDB](https://img.shields.io/badge/Warehouse-DuckDB-yellow)](https://duckdb.org/)
[![Parquet](https://img.shields.io/badge/Storage-Parquet-blue)](https://parquet.apache.org/)
[![Pytest](https://img.shields.io/badge/Testing-Pytest-green)](https://pytest.org/)
[![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-black)](https://github.com/features/actions)

> A small, free, end-to-end Data Engineering project demonstrating API ingestion, data quality, transformation, analytical warehousing, SQL analytics, automated testing and CI.

---

## Project Overview

This project demonstrates how to build a practical Data Engineering pipeline using free and open-source technologies.

The pipeline follows:

```text
Weather API
    |
    v
Python Ingestion
    |
    v
Raw JSON
    |
    v
Data Validation
    |
    v
Parquet
    |
    v
DuckDB Warehouse
    |
    v
SQL Analytics
    |
    v
Automated Tests
    |
    v
GitHub Actions CI
```

The project is designed to be:

- Free to run
- Local-first
- Beginner-friendly
- Portfolio-ready
- Reproducible
- Easy to extend
- Suitable for students learning Data Engineering

---

## Data Source

Weather data is collected from the Open-Meteo API.

### Cities

| City | Country |
|---|---|
| Dublin | Ireland |
| London | United Kingdom |
| Mumbai | India |
| Singapore | Singapore |
| Dubai | UAE |

---

## Architecture

```text
                         Open-Meteo API
                               |
                               v
                    +----------------------+
                    |  Python Ingestion    |
                    |  REST API Requests   |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |      Raw JSON        |
                    |      data/raw/       |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |   Data Validation    |
                    |   Python + Pytest    |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |       Parquet        |
                    |   data/processed/    |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |       DuckDB         |
                    |  Analytical Warehouse|
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |     SQL Analytics    |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |    GitHub Actions    |
                    |   Automated Testing  |
                    +----------------------+
```

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Ingestion, validation and transformation |
| Open-Meteo API | External weather data source |
| Pandas | Data manipulation |
| PyArrow | Parquet processing |
| Apache Parquet | Analytical file storage |
| DuckDB | Local analytical data warehouse |
| SQL | Analytics and warehouse queries |
| Pytest | Automated testing |
| Git | Version control |
| GitHub | Source control and collaboration |
| GitHub Actions | Continuous Integration |
| Markdown | Documentation |

---

## Project Structure

```text
end-to-end-weather-data-pipeline/
|
+-- .github/
|   +-- workflows/
|       +-- ci.yml
|
+-- config/
|   +-- cities.json
|
+-- data/
|   +-- raw/
|   |   +-- *.json
|   |
|   +-- processed/
|   |   +-- weather.parquet
|   |
|   +-- warehouse/
|       +-- weather.duckdb
|
+-- sql/
|   +-- weather_analysis.sql
|
+-- src/
|   +-- ingestion/
|   |   +-- extract_weather.py
|   |
|   +-- quality/
|   |   +-- validate_weather.py
|   |
|   +-- transformation/
|   |   +-- json_to_parquet.py
|   |
|   +-- warehouse/
|       +-- load_duckdb.py
|
+-- tests/
|   +-- test_weather_validation.py
|   +-- test_warehouse.py
|
+-- run_pipeline.py
+-- requirements.txt
+-- pytest.ini
+-- README.md
```

---

# Pipeline Stages

## 1. Extract - API Ingestion

Python requests weather data from the Open-Meteo API.

The raw API responses are saved as JSON files:

```text
data/raw/
```

Typical fields include:

```text
city
latitude
longitude
weather_time
temperature_2m
relative_humidity_2m
wind_speed_10m
weather_code
ingested_at
```

Keeping raw data creates a simple landing layer that can be inspected or reprocessed later.

---

## 2. Validate - Data Quality

The validation layer checks the incoming weather data before it reaches downstream systems.

Checks include:

- Required fields exist
- Temperature is numeric
- Humidity is valid
- Wind speed is valid
- Latitude is numeric
- Longitude is numeric
- Weather code exists

Example validation output:

```text
Missing weather field: relative_humidity_2m
Missing weather field: wind_speed_10m
Missing weather field: weather_code
Latitude must be numeric
```

### Why validation matters

A reliable Data Engineering pipeline should detect bad data before it reaches downstream storage and analytics.

---

## 3. Transform - JSON to Parquet

Validated JSON data is converted into Parquet.

```text
JSON
  |
  v
Pandas
  |
  v
PyArrow
  |
  v
Parquet
```

Output:

```text
data/processed/weather.parquet
```

### Why Parquet?

Parquet is useful for analytical workloads because it provides:

- Columnar storage
- Efficient reads
- Compression
- Efficient column selection
- Good interoperability with modern data tools

---

## 4. Warehouse - DuckDB

The Parquet dataset is loaded into DuckDB.

```text
weather.parquet
      |
      v
+------------------+
|      DuckDB      |
|    Warehouse     |
+--------+---------+
         |
         v
    fact_weather
```

### Main table

```text
fact_weather
```

### Main columns

| Column | Description |
|---|---|
| city | City name |
| latitude | Geographic latitude |
| longitude | Geographic longitude |
| ingested_at | Pipeline ingestion timestamp |
| weather_time | Weather observation timestamp |
| temperature_celsius | Temperature |
| humidity_percent | Relative humidity |
| wind_speed_kmh | Wind speed |
| weather_code | Weather condition code |

---

# Why DuckDB?

DuckDB is used as the analytical warehouse because it is:

- Free
- Open source
- Fast
- Lightweight
- SQL-based
- Local-first
- Easy to install
- Serverless for this use case

No cloud database is required.

You do not need:

```text
AWS
Azure
Snowflake
Databricks
Paid database infrastructure
```

Everything can run locally on a normal laptop.

> DuckDB is a strong choice for students and beginners who want to learn Data Warehousing and analytical SQL without paying for cloud infrastructure.

---

# Deduplication and Idempotency

The project uses:

```text
city + weather_time
```

as the business key for a weather observation.

This helps prevent duplicate business records when the same observation is ingested more than once.

A typical SQL approach is:

```sql
ROW_NUMBER() OVER (
    PARTITION BY city, weather_time
    ORDER BY ingested_at DESC
)
```

This keeps the most recent ingestion for the same business key.

### Key concept

Idempotency means that repeating a pipeline operation should not unintentionally create duplicate business data.

This is an important concept in production Data Engineering.

---

# SQL Analytics

Once the data is available in DuckDB, SQL can be used for analytics.

Example:

```sql
SELECT
    city,
    ROUND(AVG(temperature_celsius), 2) AS avg_temperature
FROM fact_weather
GROUP BY city
ORDER BY avg_temperature DESC;
```

Example result:

```text
City          Average Temperature
---------------------------------
Dubai                 30.2
Mumbai                27.6
Singapore             25.2
London                19.3
Dublin                17.5
```

Other possible analytics:

- Average temperature
- Maximum temperature
- Minimum temperature
- Average humidity
- Average wind speed
- City comparisons
- Observation counts
- Weather trends

---

# Automated Testing

The project uses Pytest for automated testing.

Current tests cover:

### Data Validation

- Valid weather data
- Missing weather fields
- Invalid latitude
- Invalid longitude

### Warehouse

- Business-key uniqueness
- Duplicate detection

Run:

```powershell
pytest -v
```

Example:

```text
tests/test_warehouse.py::test_weather_business_key_is_unique PASSED
tests/test_weather_validation.py::test_valid_weather_data PASSED
tests/test_weather_validation.py::test_missing_weather_field PASSED
tests/test_weather_validation.py::test_invalid_latitude PASSED
tests/test_weather_validation.py::test_invalid_longitude PASSED

5 passed
```

---

# CI - GitHub Actions

GitHub Actions automatically runs the tests when code is pushed to GitHub.

```text
Git Push
   |
   v
GitHub Actions
   |
   v
Checkout Repository
   |
   v
Install Python
   |
   v
Install Dependencies
   |
   v
Run Pytest
   |
   v
PASS / FAIL
```

Workflow file:

```text
.github/workflows/ci.yml
```

This demonstrates a basic Continuous Integration workflow.

---

# Run the Project Locally

## 1. Clone the repository

```bash
git clone https://github.com/sagarpitale95/end-to-end-weather-data-pipeline.git
```

## 2. Enter the project

```bash
cd end-to-end-weather-data-pipeline
```

## 3. Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

## 4. Activate the environment

```powershell
.venv\Scripts\Activate.ps1
```

## 5. Install dependencies

```powershell
pip install -r requirements.txt
```

## 6. Run the pipeline

```powershell
python run_pipeline.py
```

## 7. Run tests

```powershell
pytest -v
```

---

# Example DuckDB Query

After running the pipeline:

```sql
SELECT
    city,
    COUNT(*) AS records
FROM fact_weather
GROUP BY city
ORDER BY city;
```

Example:

```text
City          Records
---------------------
Dubai             2
Dublin            2
London            2
Mumbai            2
Singapore         2
```

---

# Project Cost

This project is designed to be free for learning and portfolio purposes.

| Component | Cost |
|---|---|
| Python | Free |
| Open-Meteo | Free for this project |
| Pandas | Free |
| PyArrow | Free |
| Parquet | Free |
| DuckDB | Free |
| Pytest | Free |
| Git | Free |
| GitHub | Free |
| GitHub Actions | Free within applicable usage limits |

No paid cloud infrastructure is required.

---

# What You Can Learn

| Data Engineering Concept | Demonstrated |
|---|---|
| REST API ingestion | Yes |
| Python data pipelines | Yes |
| Raw data layer | Yes |
| Data validation | Yes |
| Data quality | Yes |
| JSON processing | Yes |
| Parquet | Yes |
| Data transformation | Yes |
| Data Warehousing | Yes |
| DuckDB | Yes |
| SQL | Yes |
| Window functions | Yes |
| Deduplication | Yes |
| Idempotency | Yes |
| Automated testing | Yes |
| Git | Yes |
| GitHub | Yes |
| CI/CD | Yes |

---

# Learn, Experiment and Build

This repository is designed to be more than a project to read.

It is a **working Data Engineering playground**.

You can clone it, run it, understand each stage, change the code, add your own ideas, deliberately break things, fix them, and gradually turn the pipeline into something more advanced.

## Who is this for?

### New to Data Engineering

If you are comfortable with basic Python and SQL but have never built a complete data pipeline, this project gives you a simple starting point.

You can see how these pieces connect:

```text
API
  |
  v
Python
  |
  v
Raw Data
  |
  v
Validation
  |
  v
Parquet
  |
  v
DuckDB
  |
  v
SQL
  |
  v
Testing
  |
  v
CI
```

### Early-career Data Engineers

Use the existing pipeline as a base and improve it.

Try adding better error handling, incremental loading, logging, monitoring, orchestration or a dashboard.

### Experienced Engineers

Use it as a small sandbox for experimenting with architecture, data quality, performance, testing and automation without needing cloud infrastructure.

---

# Try It Yourself

The best way to learn Data Engineering is to **change the pipeline yourself**.

Start with a small change and work your way toward bigger improvements.

## Level 1 - Easy

### 1. Add another city

Add a new city to:

```text
config/cities.json
```

Run the pipeline and check whether the new city appears in DuckDB.

### 2. Add a new weather field

For example:

```text
precipitation
```

Follow the field through the entire pipeline:

```text
API
 -> Validation
 -> Parquet
 -> DuckDB
 -> SQL
 -> Tests
```

### 3. Write your own SQL query

Try questions such as:

- Which city has the highest temperature?
- Which city has the highest humidity?
- How many records exist per city?
- What is the average wind speed?
- Which city has the most weather observations?

### 4. Add a data-quality rule

Examples:

```text
Temperature must be between -50 and 60
Humidity must be between 0 and 100
Wind speed cannot be negative
Latitude must be between -90 and 90
Longitude must be between -180 and 180
```

Then write a Pytest test for the rule.

### 5. Run the pipeline twice

Run:

```powershell
python run_pipeline.py
python run_pipeline.py
```

Then inspect the warehouse.

Ask yourself:

> Did the second run create duplicates?

If it did, improve the deduplication logic.

---

# Level 2 - Intermediate

## 6. Add logging

Instead of relying only on print statements, introduce Python logging.

Capture events such as:

```text
Pipeline started
Fetching Dublin
Fetching London
Validation completed
Parquet created
DuckDB loaded
Pipeline completed
```

Also log errors.

---

## 7. Add API error handling

What happens if:

- The API is unavailable?
- A request times out?
- A city returns invalid data?
- The API returns an unexpected response?

Add:

- Timeouts
- Exception handling
- Retry logic
- Clear error messages

---

## 8. Add incremental loading

Instead of processing everything every time, only load new weather observations.

Think about:

```text
Last successful timestamp
        |
        v
Request only new data
        |
        v
Load new records
```

This introduces an important real-world Data Engineering concept:

**incremental processing.**

---

## 9. Add a pipeline configuration

Move configurable values into a configuration file.

For example:

```text
cities
API parameters
output locations
database location
```

Then the Python code does not need to be changed every time you want to modify the pipeline.

---

## 10. Add a data dictionary

Create:

```text
docs/data_dictionary.md
```

Document every warehouse column:

| Column | Type | Description | Example |
|---|---|---|---|
| city | VARCHAR | City name | Dublin |
| temperature_celsius | DOUBLE | Temperature | 14.5 |
| humidity_percent | DOUBLE | Relative humidity | 82 |
| wind_speed_kmh | DOUBLE | Wind speed | 18.2 |

This is a simple but useful Data Engineering practice.

---

# Level 3 - Advanced

## 11. Add a dashboard

Use a free tool such as Streamlit.

Create a dashboard showing:

- Temperature by city
- Humidity by city
- Wind speed
- Observation counts
- Historical trends

The dashboard can read directly from DuckDB.

---

## 12. Add orchestration

Turn the script into a scheduled pipeline.

Possible tools:

- Apache Airflow
- Prefect

Start locally before thinking about cloud deployment.

---

## 13. Add dbt

Use dbt to manage SQL transformations.

For example:

```text
Raw data
   |
   v
Staging model
   |
   v
Weather model
   |
   v
Analytics model
```

Add dbt tests for:

- Not null
- Unique
- Accepted values
- Relationships

---

## 14. Add Docker

Containerise the project.

A simple goal:

```text
docker compose up
```

should be enough to start the pipeline.

This is a good way to learn how applications and data pipelines are packaged consistently.

---

## 15. Add data quality monitoring

Introduce a data-quality layer that reports:

```text
Rows processed
Rows rejected
Duplicate rows
Null values
Invalid values
Pipeline duration
```

You can start with simple Python checks before introducing specialised tools.

---

## 16. Add pipeline metrics

Track:

```text
records_read
records_validated
records_rejected
records_loaded
pipeline_duration
```

Then store the metrics somewhere you can query.

This starts moving the project from a learning pipeline toward a more production-style pipeline.

---

# Challenge Ideas

Want to make your own version?

Try these challenges without looking for the exact solution first.

### Challenge 1

Add five more cities.

### Challenge 2

Add precipitation data.

### Challenge 3

Reject impossible weather values.

### Challenge 4

Make the pipeline safe to run multiple times.

### Challenge 5

Add retry logic when the API fails.

### Challenge 6

Create a daily weather summary table.

### Challenge 7

Create a city-level statistics table.

### Challenge 8

Add a data-quality report.

### Challenge 9

Create a Streamlit dashboard.

### Challenge 10

Schedule the pipeline.

### Challenge 11

Containerise the entire project with Docker.

### Challenge 12

Move the data layer from local storage to object storage.

### Challenge 13

Add dbt transformations.

### Challenge 14

Add a proper orchestration tool.

### Challenge 15

Deploy the pipeline to a cloud platform using a free tier where available.

---

# Build Your Own Version

You do not have to keep this project as a weather pipeline.

The same architecture can be reused with other datasets.

For example:

```text
Public API
   |
   v
Python
   |
   v
Raw JSON
   |
   v
Parquet
   |
   v
DuckDB
   |
   v
SQL
   |
   v
Analytics
```

Try replacing the weather API with:

- Public transport data
- Cryptocurrency prices
- Stock market data
- Football or sports statistics
- Government datasets
- Public health datasets
- Air quality data
- Open banking-style sample data
- E-commerce sample data
- Energy consumption data

The important part is not the weather data.

The important part is learning how to **design, build, test and improve a data pipeline**.

---

# A Suggested Learning Path

If you are completely new to Data Engineering, do not try to build everything at once.

Follow this progression:

```text
STEP 1
Run the existing pipeline
        |
        v
STEP 2
Understand the code
        |
        v
STEP 3
Add a new city
        |
        v
STEP 4
Write your own SQL
        |
        v
STEP 5
Add a data-quality rule
        |
        v
STEP 6
Add a new data field
        |
        v
STEP 7
Add logging and error handling
        |
        v
STEP 8
Make the pipeline incremental
        |
        v
STEP 9
Add a dashboard
        |
        v
STEP 10
Add orchestration / dbt / Docker
        |
        v
STEP 11
Move toward cloud technologies
```

You do not need to complete every step.

Pick one challenge, implement it, test it, document it, and then move to the next.

---

# Share What You Build

If you create your own improvement:

1. Fork the repository
2. Make your changes
3. Document what you changed
4. Add tests where appropriate
5. Share your implementation

The goal is to encourage people to **build on top of the project**, not simply copy it.

---

# Key Data Engineering Concepts

A Data Engineering pipeline is more than simply collecting data.

A robust pipeline considers:

```text
Data Source
     |
     v
Ingestion
     |
     v
Data Quality
     |
     v
Transformation
     |
     v
Storage
     |
     v
Warehouse
     |
     v
Analytics
     |
     v
Testing
     |
     v
Automation
```

The main lesson is:

> Extract -> Validate -> Transform -> Store -> Warehouse -> Analyse -> Test -> Automate

These concepts transfer directly to modern platforms such as:

- AWS
- Azure
- Google Cloud
- Snowflake
- Databricks
- Apache Spark
- Apache Airflow
- dbt

---

# Why This Project?

This project focuses on the fundamentals that appear in many real Data Engineering environments:

```text
Ingestion
Data Quality
Transformation
Storage
Warehousing
SQL
Testing
Automation
```

The technology can change, but these concepts remain useful across platforms such as:

- AWS
- Azure
- Google Cloud
- Snowflake
- Databricks
- Apache Spark
- Apache Airflow
- dbt

Start small, understand the fundamentals, and then experiment.

---

# Author

## Sagar Pitale

Data Engineering | Data Analytics 

GitHub:

https://github.com/sagarpitale95

---

# If You Find This Useful

If this project helps you learn Data Engineering:

- Star the repository
- Fork the project
- Build your own version
- Add new features
- Use it as a learning project
- Extend it into a cloud pipeline

---

## License

This project is intended for educational and portfolio purposes.
