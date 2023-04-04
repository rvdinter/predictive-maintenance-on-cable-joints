from alliander_predictive_maintenance.connection.alliander_circuit_weather_retriever import \
    AllianderCircuitWeatherRetriever
from alliander_predictive_maintenance.connection.alliander_weather_sources import AllianderWeatherSources
from alliander_predictive_maintenance.connection.circuit_factory import CircuitFactory
from alliander_predictive_maintenance.connection.csv_circuit_config_storage import CsvCircuitConfigStorage
from alliander_predictive_maintenance.connection.csv_circuit_partial_discharge_storage import \
    CsvCircuitPartialDischargeStorage
from alliander_predictive_maintenance.connection.excel_circuit_coordinates_reader import ExcelCircuitCoordinateReader
from alliander_predictive_maintenance.connection.excel_failed_joints_reader import ExcelFailedJointsReader
from alliander_predictive_maintenance.connection.excel_joints_with_partial_discharge_seasonality_reader import \
    ExcelJointsWithPartialDischargeSeasonalityReader
from alliander_predictive_maintenance.connection.s3_merged_circuit_storage import S3MergedCircuitStorage
from unit.test_csv_circuit_config_storage import tmp_circuit_circuit_config_root
from unit.test_csv_circuit_partial_discharge_storage import tmp_circuit_partial_discharge_data_root
from unit.test_excel_circuit_coordinate_reader import tmp_circuit_coordinates_path
from unit.test_excel_failed_joints_reader import tmp_failedjoints_path
from unit.test_excel_joints_with_partial_discharge_seasonality_reader import \
    tmp_joints_with_partial_discharge_seasonality_path
from unit.test_s3_merged_circuit_storage import mocked_get_datadump, MockedMergedCircuit
from alliander_predictive_maintenance.constants import TEST_CIRCUIT_IDS


class TestCircuitFactory:
    def test_create_circuit__valid_circuit_id__circuit_returned(self, monkeypatch, tmp_circuit_circuit_config_root,
                                                                tmp_circuit_partial_discharge_data_root,
                                                                tmp_failedjoints_path, tmp_circuit_coordinates_path,
                                                                tmp_joints_with_partial_discharge_seasonality_path):
        config = {}
        csv_circuit_config_storage = CsvCircuitConfigStorage(tmp_circuit_circuit_config_root)
        csv_circuit_partial_discharge_data_storage = CsvCircuitPartialDischargeStorage(
            tmp_circuit_partial_discharge_data_root)
        excel_failed_joints_reader = ExcelFailedJointsReader()
        excel_failed_joints_reader.load(tmp_failedjoints_path)
        excel_circuit_coordinate_reader = ExcelCircuitCoordinateReader()
        excel_circuit_coordinate_reader.load(tmp_circuit_coordinates_path)
        excel_joints_with_partial_discharge_reader = ExcelJointsWithPartialDischargeSeasonalityReader()
        excel_joints_with_partial_discharge_reader.load(tmp_joints_with_partial_discharge_seasonality_path)

        monkeypatch.setattr("alliander_predictive_maintenance.connection.s3_merged_circuit_storage.get_datadump_s3",
            mocked_get_datadump)
        monkeypatch.setattr("alliander_predictive_maintenance.connection.s3_merged_circuit_storage.MergedCircuit",
            MockedMergedCircuit)
        s3_merged_circuit_storage = S3MergedCircuitStorage()
        s3_merged_circuit_storage.load_data_dump()
        alliander_circuit_weather_retriever = AllianderCircuitWeatherRetriever(AllianderWeatherSources.CDS)

        circuit_factory = CircuitFactory(config=config, circuit_coordinates_reader=excel_circuit_coordinate_reader,
                                         weather_retriever=alliander_circuit_weather_retriever,
                                         csv_circuit_config_reader=csv_circuit_config_storage,
                                         s3_circuit_config_storage=s3_merged_circuit_storage,
                                         s3_merged_circuit_storage=s3_merged_circuit_storage,
                                         csv_partial_discharge_storage=csv_circuit_partial_discharge_data_storage)
        circuit_id = TEST_CIRCUIT_IDS[0]
        circuit = circuit_factory.create_circuit(circuit_id)
        assert circuit.circuit_id == circuit_id
