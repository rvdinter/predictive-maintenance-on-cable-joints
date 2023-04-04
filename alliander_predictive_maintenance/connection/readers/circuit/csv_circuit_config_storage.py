import os
from pathlib import Path

import pandas as pd

from alliander_predictive_maintenance.connection.readers.abstraction.dataframe_validator import DataFrameValidator
from alliander_predictive_maintenance.connection.readers.circuit.icircuit_config_reader import ICircuitConfigReader
from alliander_predictive_maintenance.constants import INVALID_PATH, COLUMNS_DO_NOT_MATCH_MANDATORY, \
    CIRCUIT_CONFIG_FILE_NOT_FOUND


class CsvCircuitConfigStorage(ICircuitConfigReader, DataFrameValidator):
    """
    A class for loading cable config data from a csv file
    """
    def __init__(self, circuit_config_absolute_root_folder: Path):
        if not circuit_config_absolute_root_folder.is_dir():
            raise ValueError(INVALID_PATH.format(path=circuit_config_absolute_root_folder))
        self.circuit_config_absolute_root_folder = circuit_config_absolute_root_folder

    def get_circuit_config(self, circuit_id: str) -> pd.DataFrame:
        return self.__read_circuit_config_csv_file(circuit_id)

    def __read_circuit_config_csv_file(self, circuit_id: str) -> pd.DataFrame:
        """Read the Circuit Config CSV file

        :param circuit_id: the circuit id to load
        """
        absolute_data_file_path = self.circuit_config_absolute_root_folder / f"{circuit_id}.csv"
        if not os.path.isfile(absolute_data_file_path):
            raise FileNotFoundError(CIRCUIT_CONFIG_FILE_NOT_FOUND.format(path=absolute_data_file_path))

        data_frame = pd.read_csv(absolute_data_file_path)
        if not self._data_frame_has_valid_structure(data_frame, self.MANDATORY_COLUMNS):
            raise TypeError(f"{COLUMNS_DO_NOT_MATCH_MANDATORY} {self.MANDATORY_COLUMNS}")
        return data_frame
