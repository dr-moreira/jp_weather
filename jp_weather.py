# -*- coding: utf-8 -*-
# Copyright 2024-2025 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pathlib import Path

import streamlit as st
import altair as alt
import pandas as pd

DATA_PATH = Path(__file__).parent / "data" / "jp_weather.csv"


@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH, parse_dates=["date"])


full_df = load_data()

st.set_page_config(
    # Title and icon for the browser's tab bar:
    page_title="João Pessoa Weather",
    page_icon="🌴",
    # Make the content take up the width of the page:
    layout="wide",
)


"""
# João Pessoa Weather

Let's explore daily weather in [João Pessoa, Paraíba,
Brazil](https://en.wikipedia.org/wiki/Jo%C3%A3o_Pessoa), sourced from the free
[Open-Meteo Historical Weather API](https://open-meteo.com/)!
"""

""  # Add a little vertical space. Same as st.write("").
""

"""
## 2024 Summary
"""

""

df_2024 = full_df[full_df["date"].dt.year == 2024]
df_2023 = full_df[full_df["date"].dt.year == 2023]

max_temp_2024 = df_2024["temp_max"].max()
max_temp_2023 = df_2023["temp_max"].max()

min_temp_2024 = df_2024["temp_min"].min()
min_temp_2023 = df_2023["temp_min"].min()

max_wind_2024 = df_2024["wind"].max()
max_wind_2023 = df_2023["wind"].max()

min_wind_2024 = df_2024["wind"].min()
min_wind_2023 = df_2023["wind"].min()

max_prec_2024 = df_2024["precipitation"].max()
max_prec_2023 = df_2023["precipitation"].max()

min_prec_2024 = df_2024["precipitation"].min()
min_prec_2023 = df_2023["precipitation"].min()


with st.container(horizontal=True, gap="medium"):
    cols = st.columns(2, gap="medium", width=300)

    with cols[0]:
        st.metric(
            "Max tempearture",
            f"{max_temp_2024:0.1f}C",
            delta=f"{max_temp_2024 - max_temp_2023:0.1f}C",
            width="content",
        )

    with cols[1]:
        st.metric(
            "Min tempearture",
            f"{min_temp_2024:0.1f}C",
            delta=f"{min_temp_2024 - min_temp_2023:0.1f}C",
            width="content",
        )

    cols = st.columns(2, gap="medium", width=300)

    with cols[0]:
        st.metric(
            "Max precipitation",
            f"{max_prec_2024:0.1f}C",
            delta=f"{max_prec_2024 - max_prec_2023:0.1f}C",
            width="content",
        )

    with cols[1]:
        st.metric(
            "Min precipitation",
            f"{min_prec_2024:0.1f}C",
            delta=f"{min_prec_2024 - min_prec_2023:0.1f}C",
            width="content",
        )

    cols = st.columns(2, gap="medium", width=300)

    with cols[0]:
        st.metric(
            "Max wind",
            f"{max_wind_2024:0.1f}m/s",
            delta=f"{max_wind_2024 - max_wind_2023:0.1f}m/s",
            width="content",
        )

    with cols[1]:
        st.metric(
            "Min wind",
            f"{min_wind_2024:0.1f}m/s",
            delta=f"{min_wind_2024 - min_wind_2023:0.1f}m/s",
            width="content",
        )

    cols = st.columns(2, gap="medium", width=300)

    weather_icons = {
        "sun": "☀️",
        "rain": "💧",
        "fog": "😶‍🌫️",
        "drizzle": "🌧️",
        "thunderstorm": "⛈️",
    }

    with cols[0]:
        weather_name = (
            full_df["weather"].value_counts().head(1).reset_index()["weather"][0]
        )
        st.metric(
            "Most common weather",
            f"{weather_icons[weather_name]} {weather_name.upper()}",
        )

    with cols[1]:
        weather_name = (
            full_df["weather"].value_counts().tail(1).reset_index()["weather"][0]
        )
        st.metric(
            "Least common weather",
            f"{weather_icons[weather_name]} {weather_name.upper()}",
        )

""
""

"""
## Compare different years
"""

YEARS = full_df["date"].dt.year.unique()
selected_years = st.pills(
    "Years to compare", YEARS, default=YEARS, selection_mode="multi"
)

if not selected_years:
    st.warning("You must select at least 1 year.", icon=":material/warning:")

df = full_df[full_df["date"].dt.year.isin(selected_years)]

cols = st.columns([3, 1])

with cols[0].container(border=True, height="stretch"):
    "### Temperature"

    st.altair_chart(
        alt.Chart(df)
        .mark_bar(width=1)
        .encode(
            alt.X("date", timeUnit="monthdate").title("date"),
            alt.Y("temp_max").title("temperature range (C)"),
            alt.Y2("temp_min"),
            alt.Color("date:N", timeUnit="year").title("year"),
            alt.XOffset("date:N", timeUnit="year"),
        )
        .configure_legend(orient="bottom")
    )

with cols[1].container(border=True, height="stretch"):
    "### Weather distribution"

    st.altair_chart(
        alt.Chart(df)
        .mark_arc()
        .encode(
            alt.Theta("count()"),
            alt.Color("weather:N"),
        )
        .configure_legend(orient="bottom")
    )


cols = st.columns(2)

with cols[0].container(border=True, height="stretch"):
    "### Wind"

    st.altair_chart(
        alt.Chart(df)
        .transform_window(
            avg_wind="mean(wind)",
            std_wind="stdev(wind)",
            frame=[0, 14],
            groupby=["monthdate(date)"],
        )
        .mark_line(size=1)
        .encode(
            alt.X("date", timeUnit="monthdate").title("date"),
            alt.Y("avg_wind:Q").title("average wind past 2 weeks (m/s)"),
            alt.Color("date:N", timeUnit="year").title("year"),
        )
        .configure_legend(orient="bottom")
    )

with cols[1].container(border=True, height="stretch"):
    "### Precipitation"

    st.altair_chart(
        alt.Chart(df)
        .mark_bar()
        .encode(
            alt.X("date:N", timeUnit="month").title("date"),
            alt.Y("precipitation:Q").aggregate("sum").title("precipitation (mm)"),
            alt.Color("date:N", timeUnit="year").title("year"),
        )
        .configure_legend(orient="bottom")
    )

cols = st.columns(2)

with cols[0].container(border=True, height="stretch"):
    "### Monthly weather breakdown"
    ""

    st.altair_chart(
        alt.Chart(df)
        .mark_bar()
        .encode(
            alt.X("month(date):O", title="month"),
            alt.Y("count():Q", title="days").stack("normalize"),
            alt.Color("weather:N"),
        )
        .configure_legend(orient="bottom")
    )

with cols[1].container(border=True, height="stretch"):
    "### Raw data"

    st.dataframe(df)
