from pathlib import Path

import pandas as pd

from alliander_predictive_maintenance.conversion.data_types.circuit_coordinate import CircuitCoordinate
from alliander_predictive_maintenance.connection.readers.circuit.icircuit_coordinates_reader import ICircuitCoordinatesReader
from alliander_predictive_maintenance.connection.readers.abstraction.iexcel_reader import IExcelReader
from alliander_predictive_maintenance.constants import COLUMNS_DO_NOT_MATCH_MANDATORY, IEXCEL_READER_LOAD_NOT_CALLED, \
    CIRCUIT_ID_NOT_IN_DATAFRAME


class ExcelCircuitCoordinateReader(ICircuitCoordinatesReader, IExcelReader):
    """Read the CircuitCoordinates from Excel"""
    def __init__(self):
        self.__circuit_coordinates_data_frame = None

    def load(self, absolute_data_file_path: Path) -> None:
        """Load in the data set

        :param absolute_data_file_path: path to the data file
        """
        data_frame = pd.read_excel(absolute_data_file_path,
                                   parse_dates=[self.DATE_SAVED_COLUMN],
                                   dtype={self.X_COORDINATE_COLUMN: float,
                                          self.Y_COORDINATE_COLUMN: float,
                                          self.CIRCUIT_ID_COLUMN: int}
                                   )
        if not self._data_frame_has_valid_structure(data_frame, self.MANDATORY_COLUMNS):
            raise TypeError(f"{COLUMNS_DO_NOT_MATCH_MANDATORY} {self.MANDATORY_COLUMNS}")

        # drop rows with empty cells, sort by date and keep only the last entries if there are multiple for one circuit
        data_frame = data_frame.dropna()
        data_frame = data_frame.sort_values(by=self.DATE_SAVED_COLUMN)
        self.__circuit_coordinates_data_frame = data_frame.drop_duplicates(subset=self.CIRCUIT_ID_COLUMN, keep="last").copy()

        # create a circuit coordinate object for each row in the dataframe and add it to another column
        self.__circuit_coordinates_data_frame[self.CIRCUIT_COORDINATES_COLUMN] = self.__circuit_coordinates_data_frame.apply(
            lambda row: CircuitCoordinate(row[self.X_COORDINATE_COLUMN],
                                          row[self.Y_COORDINATE_COLUMN],
                                          row[self.CIRCUIT_ID_COLUMN]), axis=1)

    def get_circuit_coordinate(self, circuit_id: int) -> CircuitCoordinate:
        """Get a CircuitCoordinate of a given circuit

        :param circuit_id: id of the circuit
        """
        if not self._data_frame_is_loaded(self.__circuit_coordinates_data_frame):
            raise TypeError(IEXCEL_READER_LOAD_NOT_CALLED)
        if not self._circuit_id_exists(self.__circuit_coordinates_data_frame, circuit_id, self.CIRCUIT_ID_COLUMN):
            raise ValueError(CIRCUIT_ID_NOT_IN_DATAFRAME.format(circuit_id=circuit_id))

        selected_circuit_coordinate = self.__circuit_coordinates_data_frame[
            self.__circuit_coordinates_data_frame[self.CIRCUIT_ID_COLUMN] == circuit_id]
        selected_circuit_coordinate_object = selected_circuit_coordinate[self.CIRCUIT_COORDINATES_COLUMN].iloc[0]
        return selected_circuit_coordinate_object
