from typing import Optional

import numpy as np
import pandas as pd

from alliander_predictive_maintenance.conversion.data_types.circuit_coordinate import CircuitCoordinate
from alliander_predictive_maintenance.connection.readers.circuit.icircuit_partial_discharge_reader import ICircuitPartialDischargeReader
from alliander_predictive_maintenance.conversion.data_types.joint import Joint
from alliander_predictive_maintenance.conversion.data_types.time_window import TimeWindow
from alliander_predictive_maintenance.constants import INVALID_JOINT_LOCATION, INVALID_TIME_WINDOW


class Circuit:
    """ An object representing a Circuit consisting of joints """
    def __init__(self, circuit_id: int, weather: pd.DataFrame, circuit_coordinate: CircuitCoordinate,
                 partial_discharge: pd.DataFrame, time_window: TimeWindow, circuit_length: float):
        self.__circuit_id = circuit_id
        self.__weather = weather
        self.__circuit_coordinate = circuit_coordinate
        self.__partial_discharge = partial_discharge
        self.__time_window = time_window
        self.__circuit_length = circuit_length

    @property
    def circuit_id(self):
        return self.__circuit_id

    @property
    def weather(self) -> pd.DataFrame:
        return self.__weather

    @property
    def time_window(self):
        return self.__time_window

    def create_joint(self, location: float, time_window: TimeWindow,
                     resampling_strategy: Optional[str] = "sum") -> Joint:
        """ Create a Joint object

        :param location: location in the circuit
        :param time_window: a time window of activity
        :param resampling_strategy: how to resample the partial discharge data, options are [sum, count]
        :return: a Joint object
        """
        if not 0 < location < self.__circuit_length:
            raise ValueError(INVALID_JOINT_LOCATION.format(location=location, circuit_length=self.__circuit_length))
        partial_discharge = self.__get_partial_discharge_at_location(location=location,
                                                                     resampling_strategy=resampling_strategy)
        if time_window.start_date < partial_discharge.index.min() or time_window.end_date > partial_discharge.index.max():
            raise ValueError(INVALID_TIME_WINDOW.format(time_window=time_window,
                                                        min=partial_discharge.index.min(),
                                                        max=partial_discharge.index.max()))
        partial_discharge = partial_discharge[time_window.start_date:time_window.end_date]
        return Joint(location, partial_discharge)

    def __get_partial_discharge_at_location(self, location: float, bandwidth: Optional[float] = 0.01,
                                            resampling_strategy: Optional[str] = "sum",
                                            time_resolution: Optional[str] = "1H") -> pd.Series:
        """ Get partial discharge at a specific location

        :param location: location of the partial discharge
        :param bandwidth: bandwidth of the recordings
        :param resampling_strategy: how to resample the partial discharge data, options are [sum, count]
        :param time_resolution: time resolution of the resampling
        :return: a pd.Series of partial discharge
        """
        pdframe = self.__partial_discharge.copy()
        pdframe = pdframe.dropna()

        charge = np.where(
            abs(location - pdframe[ICircuitPartialDischargeReader.LOCATION_COLUMN]) /
            self.__circuit_length <= bandwidth,
            pdframe[ICircuitPartialDischargeReader.PARTIAL_DISCHARGE_DATA_COLUMN],
            0,
        )

        if resampling_strategy == "sum":
            if time_resolution == "1min":
                return pd.Series(charge, index=pdframe[ICircuitPartialDischargeReader.DATETIME_COLUMN])
            else:
                return pd.Series(charge, index=pdframe[ICircuitPartialDischargeReader.DATETIME_COLUMN]).resample(
                    time_resolution).sum()
        elif resampling_strategy == "count":
            return (
                pd.Series(charge, index=pdframe[ICircuitPartialDischargeReader.DATETIME_COLUMN])
                .resample(time_resolution)
                .apply(np.count_nonzero)
            )
