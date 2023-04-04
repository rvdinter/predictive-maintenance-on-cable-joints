import pandas as pd
from scg_analytics.circuit import MergedCircuit
from scg_analytics.datadump import DataDump, get_datadump_s3

from alliander_predictive_maintenance.connection.readers.circuit.icircuit_config_reader import ICircuitConfigReader
from alliander_predictive_maintenance.connection.readers.circuit.icircuit_partial_discharge_reader import ICircuitPartialDischargeReader
from alliander_predictive_maintenance.constants import CIRCUIT_ID_NOT_IN_DATAFRAME, DATADUMP_NOT_LOADED


class S3MergedCircuitStorage(ICircuitPartialDischargeReader, ICircuitConfigReader):
    """
    A class for loading partial discharge data from Alliander datastores in AWS S3
    """

    def __init__(self):
        self.__datadump = None
        self.__merged_circuit = None

    def load_data_dump(self) -> None:
        """ Load a data dump from the S3 bucket """
        self.__datadump: DataDump = get_datadump_s3()

    def get_partial_discharge_data_for_circuit(self, circuit_id: str) -> pd.DataFrame:
        self.__check_data_dump()
        self.__check_circuit_id(circuit_id)
        self.__create_merged_circuit(circuit_id)
        return self.__merged_circuit.pd

    def get_circuit_config(self, circuit_id: str) -> pd.DataFrame:
        self.__check_data_dump()
        self.__check_circuit_id(circuit_id)
        self.__create_merged_circuit(circuit_id)
        return self.__merged_circuit.cableconfig

    def __create_merged_circuit(self, circuit_id: str) -> None:
        """ Create a MergedCircuit Object

        :param circuit_id: circuit id of MergedCircuit to create
        """
        if self.__merged_circuit is None or circuit_id != self.__merged_circuit.circuitnr:
            merged_circuit = MergedCircuit(circuit_id, self.__datadump.data_store)
            merged_circuit.build_pd()
            merged_circuit.build_cableconfig()
            self.__merged_circuit = merged_circuit

    def __check_data_dump(self) -> None:
        """ Check if the data dump is loaded """
        if self.__datadump is None:
            raise TypeError(DATADUMP_NOT_LOADED)

    def __check_circuit_id(self, circuit_id: str) -> None:
        """ Check if the circuit id is in the dataframe """
        if circuit_id not in self.__datadump.circuit_dict.keys():
            raise ValueError(CIRCUIT_ID_NOT_IN_DATAFRAME.format(circuit_id=circuit_id))
