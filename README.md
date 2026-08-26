# Streamlit João Pessoa Weather dashboard

An example Streamlit dashboard exploring daily weather in João Pessoa,
Paraíba, Brazil, sourced from the free
[Open-Meteo Historical Weather API](https://open-meteo.com/).

## View it in one click

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://jp-weather.streamlit.app/)

## Try it on your machine

1. Get the code:

   ```sh
   $ git clone https://github.com/dr-moreira/jp_weather.git
   ```

2. Start a virtual environment and get the dependencies (requires uv):

   ```sh
   $ uv venv

   $ .venv/bin/activate

   $ uv sync
   ```

3. (Optional) Refresh the dataset from Open-Meteo:

    ```sh
    $ uv run python scripts/fetch_data.py
    ```

4. Start the app:

    ```sh
    $ streamlit run jp_weather.py
    ```
