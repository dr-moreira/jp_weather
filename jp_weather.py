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
    page_title="Clima em João Pessoa",
    page_icon="🌴",
    # Make the content take up the width of the page:
    layout="wide",
)


"""
# Clima em João Pessoa

Vamos explorar o clima diário em [João Pessoa, Paraíba,
Brasil](https://pt.wikipedia.org/wiki/Jo%C3%A3o_Pessoa), obtido gratuitamente
pela [API de Histórico Meteorológico Open-Meteo](https://open-meteo.com/)!
"""

""  # Add a little vertical space. Same as st.write("").
""

"""
## Resumo de 2024
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
            "Temperatura máxima",
            f"{max_temp_2024:0.1f}C",
            delta=f"{max_temp_2024 - max_temp_2023:0.1f}C",
            width="content",
        )

    with cols[1]:
        st.metric(
            "Temperatura mínima",
            f"{min_temp_2024:0.1f}C",
            delta=f"{min_temp_2024 - min_temp_2023:0.1f}C",
            width="content",
        )

    cols = st.columns(2, gap="medium", width=300)

    with cols[0]:
        st.metric(
            "Precipitação máxima",
            f"{max_prec_2024:0.1f}C",
            delta=f"{max_prec_2024 - max_prec_2023:0.1f}C",
            width="content",
        )

    with cols[1]:
        st.metric(
            "Precipitação mínima",
            f"{min_prec_2024:0.1f}C",
            delta=f"{min_prec_2024 - min_prec_2023:0.1f}C",
            width="content",
        )

    cols = st.columns(2, gap="medium", width=300)

    with cols[0]:
        st.metric(
            "Vento máximo",
            f"{max_wind_2024:0.1f}m/s",
            delta=f"{max_wind_2024 - max_wind_2023:0.1f}m/s",
            width="content",
        )

    with cols[1]:
        st.metric(
            "Vento mínimo",
            f"{min_wind_2024:0.1f}m/s",
            delta=f"{min_wind_2024 - min_wind_2023:0.1f}m/s",
            width="content",
        )

    cols = st.columns(2, gap="medium", width=300)

    weather_icons = {
        "sol": "☀️",
        "chuva": "💧",
        "neblina": "😶‍🌫️",
        "garoa": "🌧️",
        "tempestade": "⛈️",
    }

    with cols[0]:
        weather_name = (
            full_df["weather"].value_counts().head(1).reset_index()["weather"][0]
        )
        st.metric(
            "Clima mais comum",
            f"{weather_icons[weather_name]} {weather_name.upper()}",
        )

    with cols[1]:
        weather_name = (
            full_df["weather"].value_counts().tail(1).reset_index()["weather"][0]
        )
        st.metric(
            "Clima menos comum",
            f"{weather_icons[weather_name]} {weather_name.upper()}",
        )

""
""

"""
## Comparar diferentes anos
"""

YEARS = full_df["date"].dt.year.unique()
selected_years = st.pills(
    "Anos para comparar", YEARS, default=YEARS, selection_mode="multi"
)

if not selected_years:
    st.warning("Você deve selecionar pelo menos 1 ano.", icon=":material/warning:")

df = full_df[full_df["date"].dt.year.isin(selected_years)]

cols = st.columns([3, 1])

with cols[0].container(border=True, height="stretch"):
    "### Temperatura"

    st.altair_chart(
        alt.Chart(df)
        .mark_bar(width=1)
        .encode(
            alt.X("date", timeUnit="monthdate").title("data"),
            alt.Y("temp_max").title("faixa de temperatura (C)"),
            alt.Y2("temp_min"),
            alt.Color("date:N", timeUnit="year").title("ano"),
            alt.XOffset("date:N", timeUnit="year"),
        )
        .configure_legend(orient="bottom")
    )

with cols[1].container(border=True, height="stretch"):
    "### Distribuição do clima"

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
    "### Vento"

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
            alt.X("date", timeUnit="monthdate").title("data"),
            alt.Y("avg_wind:Q").title("vento médio nas últimas 2 semanas (m/s)"),
            alt.Color("date:N", timeUnit="year").title("ano"),
        )
        .configure_legend(orient="bottom")
    )

with cols[1].container(border=True, height="stretch"):
    "### Precipitação"

    st.altair_chart(
        alt.Chart(df)
        .mark_bar()
        .encode(
            alt.X("date:N", timeUnit="month").title("data"),
            alt.Y("precipitation:Q").aggregate("sum").title("precipitação (mm)"),
            alt.Color("date:N", timeUnit="year").title("ano"),
        )
        .configure_legend(orient="bottom")
    )

cols = st.columns(2)

with cols[0].container(border=True, height="stretch"):
    "### Clima mensal"
    ""

    st.altair_chart(
        alt.Chart(df)
        .mark_bar()
        .encode(
            alt.X("month(date):O", title="mês"),
            alt.Y("count():Q", title="dias").stack("normalize"),
            alt.Color("weather:N"),
        )
        .configure_legend(orient="bottom")
    )

with cols[1].container(border=True, height="stretch"):
    "### Dados brutos"

    st.dataframe(df)
