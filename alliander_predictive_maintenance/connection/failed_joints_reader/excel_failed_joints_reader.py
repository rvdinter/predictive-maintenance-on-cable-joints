from pathlib import Path

import pandas as pd

from alliander_predictive_maintenance.connection.readers.abstraction.iexcel_reader import IExcelReader
from alliander_predictive_maintenance.connection.failed_joints_reader.ifailed_joints_reader import IFailedJointsReader
from alliander_predictive_maintenance.constants import COLUMNS_DO_NOT_MATCH_MANDATORY, IEXCEL_READER_LOAD_NOT_CALLED, \
    CIRCUIT_ID_NOT_IN_DATAFRAME, FAILED_JOINTS_PRIORITY, FAILED_JOINTS_LOCATION_FRACTIONAL_TIME


class ExcelFailedJointsReader(IFailedJointsReader, IExcelReader):
    """Read the failed joints from Excel."""
    def __init__(self):
        self.__failed_joints_data_frame = None

    def load(self, absolute_data_file_path: Path) -> None:
        data_frame = pd.read_excel(absolute_data_file_path,
                                   parse_dates=[self.DATETIME_COLUMN],
                                   dtype={self.LOCATION_FRACTIONAL_TIME_COLUMN: float,
                                          self.LOCATION_COLUMN: float,
                                          self.CIRCUIT_ID_COLUMN: int,
                                          self.PRIORITY_COLUMN: float})
        if not self._data_frame_has_valid_structure(data_frame, self.MANDATORY_COLUMNS):
            raise TypeError(f"{COLUMNS_DO_NOT_MATCH_MANDATORY} {self.MANDATORY_COLUMNS}")
        data_frame.dropna(subset=self.DATETIME_COLUMN, inplace=True)
        data_frame = data_frame[data_frame[self.LOCATION_COLUMN] > 0]
        self.__failed_joints_data_frame = data_frame.set_index(self.DATETIME_COLUMN)

    def get_failed_joints_for_circuit(self, circuit_id) -> pd.DataFrame:
        if not self._data_frame_is_loaded(self.__failed_joints_data_frame):
            raise TypeError(IEXCEL_READER_LOAD_NOT_CALLED)
        if not self._circuit_id_exists(self.__failed_joints_data_frame, circuit_id, self.CIRCUIT_ID_COLUMN):
            raise ValueError(CIRCUIT_ID_NOT_IN_DATAFRAME.format(circuit_id=circuit_id))

        failed_joints = self.__failed_joints_data_frame[
            (self.__failed_joints_data_frame[self.CIRCUIT_ID_COLUMN] == circuit_id)]
        return failed_joints[[self.CIRCUIT_ID_COLUMN, self.LOCATION_COLUMN]]
