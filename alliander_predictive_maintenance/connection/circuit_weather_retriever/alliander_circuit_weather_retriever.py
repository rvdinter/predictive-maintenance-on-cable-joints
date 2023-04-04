import io

import pandas as pd
import requests

from alliander_predictive_maintenance.connection.circuit_weather_retriever.alliander_weather_sources import \
    AllianderWeatherSources
from alliander_predictive_maintenance.connection.circuit_weather_retriever.icircuit_weather_retriever import \
    ICircuitWeatherRetriever
from alliander_predictive_maintenance.constants import INVALID_ENUM_INPUT, HTTP_ERROR_COULD_NOT_GET_DATA
from alliander_predictive_maintenance.conversion.data_types.circuit_coordinate import CircuitCoordinate
from alliander_predictive_maintenance.conversion.data_types.time_window import TimeWindow


class AllianderCircuitWeatherRetriever(ICircuitWeatherRetriever):
    def __init__(self, alliander_weather_source: AllianderWeatherSources):
        """
        Initialize the CircuitWeather class.

        Args:
            :param alliander_weather_source: either Climate Data Storage or KNMI weather data from the Alliander Weather API
        """
        super().__init__()
        self.__weather_api = r"https://weather.appx.cloud/api/v2"
        if alliander_weather_source == AllianderWeatherSources.KNMI:
            self.__source_id = "knmi"
            self.__model_id = "daggegevens"
        elif alliander_weather_source == AllianderWeatherSources.CDS:
            self.__source_id = "cds"
            self.__model_id = "era5sl"
        else:
            raise ValueError(f"{INVALID_ENUM_INPUT}: {alliander_weather_source}")

        self.__weather_url = f"{self.__weather_api}/weather/sources/{self.__source_id}/models/{self.__model_id}"

    def get_weather(self, circuit_coordinate: CircuitCoordinate, time_window: TimeWindow) -> pd.DataFrame:
        """ Get weather from the Alliander Weather API

        :param circuit_coordinate: Rijksdriehoeks or Lat/Lon coordinates
        :param time_window: Time window of data acquisition
        :return: pandas dataframe of weather
        """
        params = {
            "begin": time_window.start_date,
            "end": time_window.end_date,
            "lat": circuit_coordinate.x,
            "lon": circuit_coordinate.y,
            "units": "human",
            "response_format": "csv"
        }
        response = requests.get(self.__weather_url, params=params)
        if response.status_code == 200:
            weather_data_frame = pd.read_csv(io.BytesIO(response.content))
            weather_data_frame.time = pd.to_datetime(weather_data_frame.time)
            return weather_data_frame
        else:
            raise requests.HTTPError(f"{HTTP_ERROR_COULD_NOT_GET_DATA}: {response.status_code} {response.content}")
