from pathlib import Path

import pandas as pd

from alliander_predictive_maintenance.connection.readers.abstraction.iexcel_reader import IExcelReader
from alliander_predictive_maintenance.connection.joints_with_partial_discharge_seasonality_reader.ijoints_with_partial_discharge_seasonality_reader import \
    IJointsWithPartialDischargeSeasonalityReader
from alliander_predictive_maintenance.constants import COLUMNS_DO_NOT_MATCH_MANDATORY, IEXCEL_READER_LOAD_NOT_CALLED


class ExcelJointsWithPartialDischargeSeasonalityReader(IJointsWithPartialDischargeSeasonalityReader, IExcelReader):
    """Read joints with seasonality in partial discharge from Excel."""

    def __init__(self):
        self.__joints_with_partial_discharge_seasonality_data_frame = None

    def load(self, absolute_data_file_path: Path) -> None:
        data_frame = pd.read_excel(absolute_data_file_path,
                                   dtype={self.LOCATION_COLUMN: float, self.CIRCUIT_ID_COLUMN: int})
        if not self._data_frame_has_valid_structure(data_frame, self.MANDATORY_COLUMNS):
            raise TypeError(f"{COLUMNS_DO_NOT_MATCH_MANDATORY} {self.MANDATORY_COLUMNS}")

        self.__joints_with_partial_discharge_seasonality_data_frame = data_frame

    def get_joints_with_partial_discharge_seasonality(self) -> pd.DataFrame:
        if not self._data_frame_is_loaded(self.__joints_with_partial_discharge_seasonality_data_frame):
            raise TypeError(IEXCEL_READER_LOAD_NOT_CALLED)
        return self.__joints_with_partial_discharge_seasonality_data_frame
