import os.path
from pathlib import Path

import pandas as pd

from alliander_predictive_maintenance.connection.readers.abstraction.dataframe_validator import DataFrameValidator
from alliander_predictive_maintenance.connection.readers.circuit.icircuit_partial_discharge_reader import ICircuitPartialDischargeReader
from alliander_predictive_maintenance.constants import COLUMNS_DO_NOT_MATCH_MANDATORY, \
    PARTIAL_DISCHARGE_DATA_FILE_NOT_FOUND, INVALID_PATH


class CsvCircuitPartialDischargeStorage(ICircuitPartialDischargeReader, DataFrameValidator):
    """
    A class for loading partial discharge data from a csv file
    """
    def __init__(self, partial_discharge_data_absolute_root_folder: Path):
        if not partial_discharge_data_absolute_root_folder.is_dir():
            raise ValueError(INVALID_PATH.format(path=partial_discharge_data_absolute_root_folder))
        self.partial_discharge_data_absolute_root_folder = partial_discharge_data_absolute_root_folder

    def get_partial_discharge_data_for_circuit(self, circuit_id: str) -> pd.DataFrame:
        return self.__read_partial_discharge_csv_file(circuit_id)

    def __read_partial_discharge_csv_file(self, circuit_id: str) -> pd.DataFrame:
        """Read the Partial Discharge CSV file

        :param circuit_id: circuit id to get the partial discharge data for
        """
        partial_discharge_data_file_path = self.partial_discharge_data_absolute_root_folder / f"{circuit_id}.csv"
        if not os.path.isfile(partial_discharge_data_file_path):
            raise FileNotFoundError(PARTIAL_DISCHARGE_DATA_FILE_NOT_FOUND.format(path=partial_discharge_data_file_path))

        data_frame = pd.read_csv(partial_discharge_data_file_path, parse_dates=[self.DATETIME_COLUMN])
        if not self._data_frame_has_valid_structure(data_frame, self.MANDATORY_COLUMNS):
            raise TypeError(f"{COLUMNS_DO_NOT_MATCH_MANDATORY} {self.MANDATORY_COLUMNS}")
        return data_frame
