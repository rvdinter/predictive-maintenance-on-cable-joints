import pytest
from scg_analytics.datadump import DataDump

from alliander_predictive_maintenance.connection.s3_merged_circuit_storage import S3MergedCircuitStorage
from unit.test_csv_circuit_config_storage import circuit_config_dataframe
from unit.test_csv_circuit_partial_discharge_storage import circuit_partial_discharge_dataframe
from alliander_predictive_maintenance.constants import TEST_CIRCUIT_IDS

CIRCUIT_LENGTH = 1503.12


def mocked_get_datadump():
    data_dump = DataDump()
    data_dump.circuit_dict = {str(TEST_CIRCUIT_ID): None for TEST_CIRCUIT_ID in TEST_CIRCUIT_IDS}
    return data_dump


class MockedMergedCircuit:
    def __init__(self, circuitnr, data_store):
        self.pd = circuit_partial_discharge_dataframe()
        self.circuitnr = circuitnr
        self.data_store = data_store
        self.circuitlength = None
        self.cableconfig = None

    def build_pd(self):
        pass

    def build_cableconfig(self):
        self.circuitlength = CIRCUIT_LENGTH
        self.cableconfig = circuit_config_dataframe()


class TestS3MergedCircuitStorage:
    def test_get_partial_discharge_data_for_circuit__circuit_id_exists__partial_discharge_returned(self, monkeypatch):
        monkeypatch.setattr(
            "alliander_predictive_maintenance.connection.s3_merged_circuit_storage.get_datadump_s3",
            mocked_get_datadump)
        monkeypatch.setattr(
            "alliander_predictive_maintenance.connection.s3_merged_circuit_storage.MergedCircuit",
            MockedMergedCircuit)
        s3_merged_circuit_storage = S3MergedCircuitStorage()
        s3_merged_circuit_storage.load_data_dump()
        for circuit_id in TEST_CIRCUIT_IDS:
            assert s3_merged_circuit_storage.get_partial_discharge_data_for_circuit(str(circuit_id)).equals(
                circuit_partial_discharge_dataframe())

    def test_get_partial_discharge_data_for_circuit__datadump_not_loaded__exception_thrown(self, monkeypatch):
        monkeypatch.setattr(
            "alliander_predictive_maintenance.connection.s3_merged_circuit_storage.get_datadump_s3",
            mocked_get_datadump)
        s3_merged_circuit_storage = S3MergedCircuitStorage()
        for circuit_id in TEST_CIRCUIT_IDS:
            with pytest.raises(TypeError):
                s3_merged_circuit_storage.get_partial_discharge_data_for_circuit(str(circuit_id))

    def test_get_partial_discharge_data_for_circuit__circuit_id_not_exists__exception_thrown(self, monkeypatch):
        monkeypatch.setattr(
            "alliander_predictive_maintenance.connection.s3_merged_circuit_storage.get_datadump_s3",
            mocked_get_datadump)
        monkeypatch.setattr(
            "alliander_predictive_maintenance.connection.s3_merged_circuit_storage.MergedCircuit",
            MockedMergedCircuit)
        s3_merged_circuit_storage = S3MergedCircuitStorage()
        s3_merged_circuit_storage.load_data_dump()
        with pytest.raises(ValueError):
            s3_merged_circuit_storage.get_partial_discharge_data_for_circuit("03")

    def test_get_get_circuit_config__circuit_id_exists__circuit_config_returned(self, monkeypatch):
        monkeypatch.setattr(
            "alliander_predictive_maintenance.connection.s3_merged_circuit_storage.get_datadump_s3",
            mocked_get_datadump)
        monkeypatch.setattr(
            "alliander_predictive_maintenance.connection.s3_merged_circuit_storage.MergedCircuit",
            MockedMergedCircuit)
        s3_merged_circuit_storage = S3MergedCircuitStorage()
        s3_merged_circuit_storage.load_data_dump()
        circuit_id = str(TEST_CIRCUIT_IDS[0])
        assert s3_merged_circuit_storage.get_circuit_config(circuit_id).equals(circuit_config_dataframe())
        assert s3_merged_circuit_storage.get_circuit_config(circuit_id).equals(circuit_config_dataframe())

    def test_get_get_circuit_config__datadump_not_loaded__exception_thrown(self, monkeypatch):
        monkeypatch.setattr(
            "alliander_predictive_maintenance.connection.s3_merged_circuit_storage.get_datadump_s3",
            mocked_get_datadump)
        s3_merged_circuit_storage = S3MergedCircuitStorage()
        for circuit_id in TEST_CIRCUIT_IDS:
            with pytest.raises(TypeError):
                s3_merged_circuit_storage.get_circuit_config(str(circuit_id))

    def test_get_get_circuit_config__circuit_id_not_exists__exception_thrown(self, monkeypatch):
        monkeypatch.setattr(
            "alliander_predictive_maintenance.connection.s3_merged_circuit_storage.get_datadump_s3",
            mocked_get_datadump)
        monkeypatch.setattr(
            "alliander_predictive_maintenance.connection.s3_merged_circuit_storage.MergedCircuit",
            MockedMergedCircuit)
        s3_merged_circuit_storage = S3MergedCircuitStorage()
        s3_merged_circuit_storage.load_data_dump()
        with pytest.raises(ValueError):
            s3_merged_circuit_storage.get_circuit_config("03")
