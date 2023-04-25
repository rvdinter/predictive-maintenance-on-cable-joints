import pandas as pd
from typing import List

from alliander_predictive_maintenance.conversion.data_types.predictive_maintenance_joint_data import PredictiveMaintenanceJointData


class WeatherAndPartialDischargeTransformer:
    def __init__(self, weather_columns: List[str], partial_discharge_column: str):
        self.partial_discharge_column = partial_discharge_column
        self.partial_discharge_and_weather_columns = weather_columns + [self.partial_discharge_column]

    def transform(self, predictive_maintenance_joint_data: PredictiveMaintenanceJointData,
                  lags: List[int], methods: List) -> PredictiveMaintenanceJointData:
        """ Transform an input dataframe to enrich its features

        :param predictive_maintenance_joint_data: historical weather and partial discharge data. Must be of same length.
        :param lags: list with numbers of lags
        :param methods: methods for moving averages
        :return: transformed  historical weather and partial discharge data.
        """
        data_frame = predictive_maintenance_joint_data.cds_weather.join(
            predictive_maintenance_joint_data.partial_discharge.rename(self.partial_discharge_column), how="right")
        data_frame_resampled = self.__resample(data_frame)
        rolling_methods = {column: methods for column in self.partial_discharge_and_weather_columns}

        lag_data_frames = []
        for lag in lags:
            lag_data_frame = data_frame_resampled.rolling(window=lag).agg(rolling_methods)
            diff_data_frame = lag_data_frame.diff()
            lag_data_frame.columns = pd.MultiIndex.from_tuples(
                [column + (f"{lag}_days",) for column in lag_data_frame.columns],
                names=["feature", "rolling", "lag"]).to_flat_index()
            diff_data_frame.columns = pd.MultiIndex.from_tuples(
                [column + (f"{lag}_days_diff",) for column in diff_data_frame.columns],
                names=["feature", "rolling", "diff"]).to_flat_index()
            lag_data_frame.columns = ["_".join(map(str, col)) for col in lag_data_frame.columns]
            diff_data_frame.columns = ["_".join(map(str, col)) for col in diff_data_frame.columns]
            lag_data_frames.extend([lag_data_frame, diff_data_frame])

        lags_data_frame = pd.concat(lag_data_frames, axis=1)
        exog = lags_data_frame.dropna()
        endog = data_frame_resampled[self.partial_discharge_column][exog.index.min():exog.index.max()]
        return PredictiveMaintenanceJointData(cds_weather=exog, knmi_weather=None, partial_discharge=endog,
                                              circuit_id=predictive_maintenance_joint_data.circuit_id,
                                              location_in_meters=predictive_maintenance_joint_data.location_in_meters)

    def __resample(self, data_frame: pd.DataFrame, resample_strategy: str = "1d") -> pd.DataFrame:
        """ Resample the data frame to another time window using the mean

        :param data_frame: data frame with weather and partial discharge information
        :param resample_strategy: time window to resample to
        :return: resampled data frame
        """
        data_frame_copy = data_frame.copy()
        data_frame_resampled = data_frame_copy.resample(resample_strategy).mean()
        return data_frame_resampled
