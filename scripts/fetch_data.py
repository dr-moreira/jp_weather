# -*- coding: utf-8 -*-
"""Fetch João Pessoa daily historical weather from Open-Meteo and save as CSV.

Data source: Open-Meteo Historical Weather API (https://open-meteo.com/),
free and keyless. Output schema mirrors the classic Seattle weather dataset:
date, precipitation (mm), temp_max (C), temp_min (C), wind (m/s), weather.
"""

import sys
from pathlib import Path

import pandas as pd
import requests

LATITUDE = -7.115
LONGITUDE = -34.861
TIMEZONE = "America/Recife"
START_DATE = "2021-01-01"
END_DATE = "2024-12-31"

OUTPUT_PATH = Path(__file__).resolve().parent.parent / "data" / "jp_weather.csv"

# WMO weather codes (https://open-meteo.com/en/docs) collapsed into the
# small set of categories the dashboard displays. João Pessoa is tropical,
# so "snow" never occurs and is omitted.
WEATHER_CODE_MAP = {
    0: "sol",
    1: "sol",
    2: "sol",
    3: "sol",
    45: "neblina",
    48: "neblina",
    51: "garoa",
    53: "garoa",
    55: "garoa",
    56: "garoa",
    57: "garoa",
    61: "chuva",
    63: "chuva",
    65: "chuva",
    66: "chuva",
    67: "chuva",
    80: "chuva",
    81: "chuva",
    82: "chuva",
    95: "tempestade",
    96: "tempestade",
    99: "tempestade",
}


def fetch() -> pd.DataFrame:
    response = requests.get(
        "https://archive-api.open-meteo.com/v1/archive",
        params={
            "latitude": LATITUDE,
            "longitude": LONGITUDE,
            "start_date": START_DATE,
            "end_date": END_DATE,
            "daily": (
                "temperature_2m_max,temperature_2m_min,"
                "precipitation_sum,windspeed_10m_max,weathercode"
            ),
            "timezone": TIMEZONE,
        },
        timeout=30,
    )
    response.raise_for_status()
    daily = response.json()["daily"]

    df = pd.DataFrame(
        {
            "date": pd.to_datetime(daily["time"]),
            "precipitation": daily["precipitation_sum"],
            "temp_max": daily["temperature_2m_max"],
            "temp_min": daily["temperature_2m_min"],
            # Open-Meteo returns km/h; convert to m/s to match the
            # original Seattle dataset's units.
            "wind": [round(v / 3.6, 1) for v in daily["windspeed_10m_max"]],
            "weather": [WEATHER_CODE_MAP.get(c, "sol") for c in daily["weathercode"]],
        }
    )
    return df


def main() -> int:
    df = fetch()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Wrote {len(df)} rows to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
