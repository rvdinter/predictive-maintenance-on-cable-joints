import abc
from typing import List

import pandas as pd


class DataFrameValidator(metaclass=abc.ABCMeta):
    def _data_frame_has_valid_structure(self, data_frame: pd.DataFrame, mandatory_columns: List[str]) -> bool:
        """ Check if the dataframe structure is valid.

        :param data_frame: dataframe to check
        """
        return set(mandatory_columns).issubset(data_frame.columns)

    def _data_frame_is_loaded(self, data_frame: pd.DataFrame) -> bool:
        """Check if the dataframe is loaded.
        """
        return data_frame is not None

    def _circuit_id_exists(self, data_frame: pd.DataFrame, circuit_id: int, circuit_id_column: str) -> bool:
        """ Check if the circuit_id exists in the column of the dataframe.

        :param circuit_id: the circuit id to check
        :param circuit_id_column: the column of the dataframe to check the circuit id for
        """
        return circuit_id in data_frame[circuit_id_column].values
