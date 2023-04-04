import abc
from typing import Optional

import pandas as pd

from alliander_predictive_maintenance.conversion.data_types.circuit_coordinate import CircuitCoordinate
from alliander_predictive_maintenance.conversion.data_types.time_window import TimeWindow


class ICircuitWeatherRetriever(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_weather') and
                callable(subclass.get_weather) or
                NotImplemented)

    def __init__(self):
        self._weather: Optional[pd.DataFrame] = None

    @abc.abstractmethod
    def get_weather(self, circuit_coordinate: CircuitCoordinate, time_window: TimeWindow) -> pd.DataFrame:
        """ Get weather of the specified API

        :param circuit_coordinate: Rijksdriehoeks or Lat/Lon coordinates
        :param time_window: Time window of data acquisition
        :return: pandas dataframe of weather
        """
        raise NotImplementedError
