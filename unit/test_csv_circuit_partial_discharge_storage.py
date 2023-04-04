from pathlib import Path

import pandas as pd
import pytest

from alliander_predictive_maintenance.connection.csv_circuit_partial_discharge_storage import \
    CsvCircuitPartialDischargeStorage
from alliander_predictive_maintenance.constants import TEST_CIRCUIT_IDS


@pytest.fixture
def tmp_circuit_partial_discharge_data_root(tmp_path) -> Path:
    partial_discharge_root = tmp_path / "PartialDischarge"
    partial_discharge_root.mkdir(parents=True, exist_ok=True)
    for circuit_id in TEST_CIRCUIT_IDS:
        data_path = partial_discharge_root / f"{circuit_id}.csv"
        circuit_partial_discharge_data_storage_to_csv(data_path)
    return partial_discharge_root


def circuit_partial_discharge_data_storage_to_csv(data_path: Path):
    df = circuit_partial_discharge_dataframe()
    df.to_csv(data_path)


def circuit_partial_discharge_dataframe():
    data = {
        CsvCircuitPartialDischargeStorage.DATETIME_COLUMN: pd.date_range(pd.Timestamp("01/01/2019"), pd.Timestamp("01/05/2019"), freq="1d"),
        CsvCircuitPartialDischargeStorage.LOCATION_COLUMN: [1, 2, 3, 4, 5],
        CsvCircuitPartialDischargeStorage.PARTIAL_DISCHARGE_DATA_COLUMN: [10, 20, 30, 10, 10],
    }
    return pd.DataFrame(data)


class TestCsvCircuitPartialDischargeStorage:
    dump_file_name = "dumped_file.csv"

    def test_init__valid_data_path_given__initialized(self, tmp_circuit_partial_discharge_data_root):
        csv_circuit_partial_discharge_storage = CsvCircuitPartialDischargeStorage(
            tmp_circuit_partial_discharge_data_root)
        assert csv_circuit_partial_discharge_storage.partial_discharge_data_absolute_root_folder == \
               tmp_circuit_partial_discharge_data_root

    def test_init__invalid_data_path_given__exception_thrown(self):
        with pytest.raises(ValueError):
            CsvCircuitPartialDischargeStorage(Path("some/invalid/path"))

    def test_get_partial_discharge_data_for_circuit__valid_circuit_given__partial_discharge_data_returned(self,
                                                                                                          tmp_circuit_partial_discharge_data_root):
        csv_circuit_partial_discharge_storage = CsvCircuitPartialDischargeStorage(
            tmp_circuit_partial_discharge_data_root)
        for circuit_id in TEST_CIRCUIT_IDS:
            partial_discharge_data = csv_circuit_partial_discharge_storage.get_partial_discharge_data_for_circuit(
                circuit_id)
            assert len(partial_discharge_data) == 5

    def test_get_partial_discharge_data_for_circuit__invalid_circuit_given__exception_thrown(self,
                                                                                             tmp_circuit_partial_discharge_data_root):
        csv_circuit_partial_discharge_storage = CsvCircuitPartialDischargeStorage(
            tmp_circuit_partial_discharge_data_root)
        with pytest.raises(FileNotFoundError):
            csv_circuit_partial_discharge_storage.get_partial_discharge_data_for_circuit("invalid_circuit")
