import pandas as pd
import pytest

from alliander_predictive_maintenance.connection.excel_failed_joints_reader import ExcelFailedJointsReader


@pytest.fixture
def tmp_failedjoints_path(tmp_path):
    data_path = tmp_path / "FailedJoints.xlsx"

    data = {
        ExcelFailedJointsReader.CIRCUIT_ID_COLUMN: [1, 2, 3, 4, 1],
        ExcelFailedJointsReader.DATETIME_COLUMN: [1, 2, 3, 4, 5],
        ExcelFailedJointsReader.PRIORITY_COLUMN: [10, 20, 30, 10, 10],
        ExcelFailedJointsReader.LOCATION_COLUMN: [1, 2, 3, 4, 5],
        ExcelFailedJointsReader.LOCATION_FRACTIONAL_TIME_COLUMN: [123, 1, 1000, 1000, 122]
    }
    df = pd.DataFrame(data)
    df.to_excel(data_path)
    return data_path


class TestExcelFailedJointsReader:
    def test_load_data_set__file_not_exists__exception_thrown(self, tmp_path):
        excel_failed_joints_reader = ExcelFailedJointsReader()
        with pytest.raises(FileNotFoundError):
            excel_failed_joints_reader.load(tmp_path / "nonexistent_file.xlsx")

    def test_get_failed_joints_for_circuit__failed_joints_exist__failed_joints_returned(self, tmp_failedjoints_path):
        excel_failed_joints_reader = ExcelFailedJointsReader()
        excel_failed_joints_reader.load(tmp_failedjoints_path)

        failed_joint_locations = excel_failed_joints_reader.get_failed_joints_for_circuit(1)
        assert len(failed_joint_locations) == 2

    def test_get_failed_joints_for_circuit__no_failed_joints_in_circuit__empty_dataframe_returned(self,
                                                                                             tmp_failedjoints_path):
        excel_failed_joints_reader = ExcelFailedJointsReader()
        excel_failed_joints_reader.load(tmp_failedjoints_path)

        for i in [2, 3, 4]:
            failed_joint_locations = excel_failed_joints_reader.get_failed_joints_for_circuit(i)
            assert len(failed_joint_locations) == 0

    def test_get_failed_joints_for_circuit__circuit_not_exists__exception_thrown(self, tmp_failedjoints_path):
        excel_failed_joints_reader = ExcelFailedJointsReader()
        excel_failed_joints_reader.load(tmp_failedjoints_path)

        with pytest.raises(ValueError):
            excel_failed_joints_reader.get_failed_joints_for_circuit(6)
