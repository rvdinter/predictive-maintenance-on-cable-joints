import pandas as pd
import pytest

from alliander_predictive_maintenance.connection.circuit_coordinate import CircuitCoordinate
from alliander_predictive_maintenance.connection.excel_circuit_coordinates_reader import ExcelCircuitCoordinateReader


@pytest.fixture
def tmp_circuit_coordinates_path(tmp_path):
    data_path = tmp_path / "CircuitCoordinates.xlsx"

    data = {
        ExcelCircuitCoordinateReader.CIRCUIT_ID_COLUMN: [1, 2, 3, 4, 1],
        ExcelCircuitCoordinateReader.DATE_SAVED_COLUMN: [1, 2, 3, 4, 5],
        ExcelCircuitCoordinateReader.X_COORDINATE_COLUMN: [10, 20, 30, 10, 10],
        ExcelCircuitCoordinateReader.Y_COORDINATE_COLUMN: [1, 2, 3, 4, 5],
    }
    df = pd.DataFrame(data)
    df.to_excel(data_path)
    return data_path


class TestExcelCircuitCoordinateReader:
    def test_load_data_set__file_not_exists__exception_thrown(self, tmp_path):
        excel_circuit_coordinate_reader = ExcelCircuitCoordinateReader()
        with pytest.raises(FileNotFoundError):
            excel_circuit_coordinate_reader.load(tmp_path / "nonexistent_file.xlsx")

    def test_get_circuit_coordinate__circuit_coordinate_exist__circuit_coordinate_returned(self,
                                                                                           tmp_circuit_coordinates_path):
        excel_circuit_coordinate_reader = ExcelCircuitCoordinateReader()
        excel_circuit_coordinate_reader.load(tmp_circuit_coordinates_path)

        circuit_coordinate = excel_circuit_coordinate_reader.get_circuit_coordinate(1)
        assert circuit_coordinate == CircuitCoordinate(10, 5, 1)

    def test_get_circuit_coordinate__circuit_not_exists__exception_thrown(self, tmp_circuit_coordinates_path):
        excel_circuit_coordinate_reader = ExcelCircuitCoordinateReader()
        excel_circuit_coordinate_reader.load(tmp_circuit_coordinates_path)

        with pytest.raises(ValueError):
            excel_circuit_coordinate_reader.get_circuit_coordinate(6)
