from pathlib import Path

import pandas as pd
import pytest

from alliander_predictive_maintenance.connection.csv_circuit_config_storage import CsvCircuitConfigStorage
from alliander_predictive_maintenance.constants import TEST_CIRCUIT_IDS


@pytest.fixture
def tmp_circuit_circuit_config_root(tmp_path) -> Path:
    circuit_config_root = tmp_path / "CircuitConfig"
    circuit_config_root.mkdir(parents=True, exist_ok=True)
    for circuit_id in TEST_CIRCUIT_IDS:
        data_path = circuit_config_root / f"{circuit_id}.csv"
        circuit_config_storage_to_csv(data_path)
    return circuit_config_root


def circuit_config_storage_to_csv(data_path: Path):
    df = circuit_config_dataframe()
    df.to_csv(data_path)


def circuit_config_dataframe():
    data = {
        CsvCircuitConfigStorage.COMPONENT_TYPE: ["RMU", "Termination", "Joint"],
        CsvCircuitConfigStorage.LENGTH: [1, 2, 3],
        CsvCircuitConfigStorage.CUMULATIVE_LENGTH: [10, 20, 30],
        CsvCircuitConfigStorage.COMPONENT_NAME: ["Leeuwarden", "Arnhem", "Apeldoorn"],
        CsvCircuitConfigStorage.DISTANCE_TO_START: [1, 2, 3],
        CsvCircuitConfigStorage.DISTANCE_TO_END: [4, 5, 6]
    }
    return pd.DataFrame(data)


class TestCsvCircuitConfigStorage:
    dump_file_name = "dumped_file.csv"

    def test_init__valid_data_path_given__initialized(self, tmp_circuit_circuit_config_root):
        csv_circuit_config_storage = CsvCircuitConfigStorage(tmp_circuit_circuit_config_root)
        assert csv_circuit_config_storage.circuit_config_absolute_root_folder == tmp_circuit_circuit_config_root

    def test_init__invalid_data_path_given__exception_thrown(self):
        with pytest.raises(ValueError):
            CsvCircuitConfigStorage(Path("some/invalid/path"))

    def test_get_circuit_config__valid_circuit_given__circuit_config_returned(self, tmp_circuit_circuit_config_root):
        csv_circuit_config_storage = CsvCircuitConfigStorage(tmp_circuit_circuit_config_root)
        for circuit_id in TEST_CIRCUIT_IDS:
            circuit_config = csv_circuit_config_storage.get_circuit_config(circuit_id)
            assert len(circuit_config) == 3

    def test_get_circuit_config__invalid_circuit_given__exception_thrown(self, tmp_circuit_circuit_config_root):
        csv_circuit_config_storage = CsvCircuitConfigStorage(tmp_circuit_circuit_config_root)
        with pytest.raises(FileNotFoundError):
            csv_circuit_config_storage.get_circuit_config("invalid_circuit")
