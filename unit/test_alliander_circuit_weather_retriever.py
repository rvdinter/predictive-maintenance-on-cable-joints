import pandas as pd
import pytest
import requests

from alliander_predictive_maintenance.connection.alliander_circuit_weather_retriever import \
    AllianderCircuitWeatherRetriever, AllianderWeatherSources
from alliander_predictive_maintenance.connection.circuit_coordinate import CircuitCoordinate
from alliander_predictive_maintenance.conversion.time_window import TimeWindow


class TestAllianderCircuitWeatherRetriever:
    def test_init__invalid_enum_input__exception_thrown(self):
        with pytest.raises(ValueError):
            AllianderCircuitWeatherRetriever("invalid input")

    @pytest.mark.parametrize("alliander_weather_sources", [AllianderWeatherSources.KNMI, AllianderWeatherSources.CDS])
    def test_get_weather__valid_input__weather_data_returned(self, alliander_weather_sources):
        alliander_circuit_weather_retriever = AllianderCircuitWeatherRetriever(alliander_weather_sources)

        circuit_coordinate = CircuitCoordinate(52.508969, 4.986738, 23108)
        time_window = TimeWindow(pd.Timestamp("01/01/2019"), pd.Timestamp("01/02/2019"))

        weather_data_frame = alliander_circuit_weather_retriever.get_weather(circuit_coordinate, time_window)
        assert type(weather_data_frame) is pd.DataFrame

    @pytest.mark.parametrize("alliander_weather_sources", [AllianderWeatherSources.KNMI, AllianderWeatherSources.CDS])
    def test_get_weather__invalid_input__exception_thrown(self, alliander_weather_sources):
        alliander_circuit_weather_retriever = AllianderCircuitWeatherRetriever(alliander_weather_sources)

        circuit_coordinate = CircuitCoordinate(52.508969, 4.986738, 23108)
        # dates are swapped
        time_window = TimeWindow(pd.Timestamp("01/02/2019"), pd.Timestamp("01/01/2019"))

        with pytest.raises(requests.HTTPError):
            alliander_circuit_weather_retriever.get_weather(circuit_coordinate, time_window)
