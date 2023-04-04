import pandas as pd
import pytest

from alliander_predictive_maintenance.connection.excel_joints_with_partial_discharge_seasonality_reader import \
    ExcelJointsWithPartialDischargeSeasonalityReader
from alliander_predictive_maintenance.connection.ijoints_with_partial_discharge_seasonality_joints import \
    IJointsWithPartialDischargeSeasonalityReader


@pytest.fixture
def tmp_joints_with_partial_discharge_seasonality_path(tmp_path):
    data_path = tmp_path / "SeasonalJoints.xlsx"

    data = {
        IJointsWithPartialDischargeSeasonalityReader.CIRCUIT_ID_COLUMN: [1, 2, 3, 4, 1],
        IJointsWithPartialDischargeSeasonalityReader.LOCATION_COLUMN: [1, 2, 3, 4, 5],
    }
    pd.DataFrame(data).to_excel(data_path)
    return data_path


class TestExcelJointsWithPartialDischargeSeasonalityReader:
    def test_load_data_set__file_not_exists__exception_thrown(self, tmp_path):
        excel_joints_with_partial_discharge_seasonality_reader = ExcelJointsWithPartialDischargeSeasonalityReader()
        with pytest.raises(FileNotFoundError):
            excel_joints_with_partial_discharge_seasonality_reader.load(tmp_path / "nonexistent_file.xlsx")

    def test_get_joints_with_partial_discharge_seasonality__data_loaded__seasonal_joints_returned(self,
                                                                                                  tmp_joints_with_partial_discharge_seasonality_path):
        excel_joints_with_partial_discharge_seasonality_reader = ExcelJointsWithPartialDischargeSeasonalityReader()
        excel_joints_with_partial_discharge_seasonality_reader.load(tmp_joints_with_partial_discharge_seasonality_path)

        assert len(
            excel_joints_with_partial_discharge_seasonality_reader.get_joints_with_partial_discharge_seasonality()) == 5

    def test_get_joints_with_partial_discharge_seasonality__data_not_loaded__exception_thrown(self,
                                                                                              tmp_joints_with_partial_discharge_seasonality_path):
        excel_joints_with_partial_discharge_seasonality_reader = ExcelJointsWithPartialDischargeSeasonalityReader()

        with pytest.raises(TypeError):
            excel_joints_with_partial_discharge_seasonality_reader.get_joints_with_partial_discharge_seasonality()
