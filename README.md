# 🌦️ End-to-End Weather Data Engineering Pipeline

![CI](https://github.com/sagarpitale95/end-to-end-weather-data-pipeline/actions/workflows/ci.yml/badge.svg)

An end-to-end Data Engineering project that ingests weather data from a public API, validates the data, transforms it into Parquet, loads it into a DuckDB analytical warehouse, and runs automated data-quality tests through GitHub Actions.

The entire project uses free and open-source technologies.

---

## 📌 Project Overview

This project demonstrates a complete modern data engineering workflow:

API → Raw JSON → Data Validation → Parquet → DuckDB → SQL Analytics → Automated Testing → CI/CD

The pipeline collects weather observations for:

- Dublin
- London
- Mumbai
- Singapore
- Dubai

Weather data is stored as raw JSON, transformed into columnar Parquet format, and loaded into a local DuckDB analytical warehouse.

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │    Open-Meteo API   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Python Ingestion    │
                    │ REST API Extraction │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Raw JSON       │
                    │      data/raw       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Data Validation   │
                    │       Pytest        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Parquet        │
                    │  data/processed     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       DuckDB        │
                    │   Analytical DWH    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    SQL Analytics    │
                    │ sql/weather_        │
                    │ analysis.sql        │
                    └─────────────────────┘

                         GitHub Actions
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Automated Testing   │
                    │      Pytest         │
                    └─────────────────────┘