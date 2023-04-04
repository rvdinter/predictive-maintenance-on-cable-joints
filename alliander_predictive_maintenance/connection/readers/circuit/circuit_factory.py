from pathlib import Path
from typing import Dict

import pandas as pd

from alliander_predictive_maintenance.connection.readers.circuit.icircuit_config_reader import ICircuitConfigReader
from alliander_predictive_maintenance.connection.readers.circuit.icircuit_coordinates_reader import ICircuitCoordinatesReader
from alliander_predictive_maintenance.connection.readers.circuit.icircuit_partial_discharge_reader import ICircuitPartialDischargeReader
from alliander_predictive_maintenance.connection.circuit_weather_retriever.icircuit_weather_retriever import ICircuitWeatherRetriever
from alliander_predictive_maintenance.conversion.data_types.circuit import Circuit
from alliander_predictive_maintenance.conversion.data_types.time_window import TimeWindow
from alliander_predictive_maintenance.constants import NOTIMPLEMENTEDERROR_AWS


class CircuitFactory:
    """ A class for creating a Circuit object """
    def __init__(self,
                 config: Dict,
                 circuit_coordinates_reader: ICircuitCoordinatesReader,
                 weather_retriever: ICircuitWeatherRetriever,
                 csv_partial_discharge_storage: ICircuitPartialDischargeReader,
                 csv_circuit_config_reader: ICircuitConfigReader):
        self.__config = config
        self.__circuit_coordinates_reader = circuit_coordinates_reader
        self.__weather_retriever = weather_retriever
        self.__csv_partial_discharge_storage = csv_partial_discharge_storage
        self.__csv_circuit_config_reader = csv_circuit_config_reader
        self._circuit_weather = None

    def create_circuit(self, circuit_id: int) -> Circuit:
        """ Create a Circuit object from an circuit ID

        :param circuit_id: ID of the circuit
        :return: Circuit object
        """
        circuit_coordinate = self.__circuit_coordinates_reader.get_circuit_coordinate(circuit_id)
        circuit_config = self.__load_circuit_config(str(circuit_id))
        circuit_length = circuit_config[ICircuitConfigReader.CUMULATIVE_LENGTH_COLUMN].max()
        partial_discharge_data = self.__load_partial_discharge_data(str(circuit_id))
        time_window = TimeWindow(partial_discharge_data[ICircuitPartialDischargeReader.DATETIME_COLUMN].min(),
                                 partial_discharge_data[ICircuitPartialDischargeReader.DATETIME_COLUMN].max())
        circuit_weather = self.__weather_retriever.get_weather(circuit_coordinate, time_window)
        return Circuit(circuit_id=circuit_id,
                       weather=circuit_weather,
                       circuit_coordinate=circuit_coordinate,
                       partial_discharge=partial_discharge_data,
                       time_window=time_window,
                       circuit_length=circuit_length)

    def __load_partial_discharge_data(self, circuit_id: str) -> pd.DataFrame:
        """ Load a partial discharge dataframe from CSV or S3

        :param circuit_id: ID of the circuit
        :return: dataframe of partial discharge
        """
        try:
            partial_discharge_data = self.__csv_partial_discharge_storage.get_partial_discharge_data_for_circuit(
                circuit_id)
        except FileNotFoundError:
            raise NotImplementedError(NOTIMPLEMENTEDERROR_AWS.format(data="partial discharge"))
        return partial_discharge_data

    def __load_circuit_config(self, circuit_id: str) -> pd.DataFrame:
        """ Load a circuit configuration from CSV or S3

        :param circuit_id: ID of the circuit
        :return: dataframe of circuit configuration
        """
        try:
            circuit_config = self.__csv_circuit_config_reader.get_circuit_config(circuit_id)
        except FileNotFoundError:
            raise NotImplementedError(NOTIMPLEMENTEDERROR_AWS.format(data="circuit config"))
        return circuit_config
