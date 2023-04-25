import numpy as np

from alliander_predictive_maintenance.conversion.data_types.predictive_maintenance_joint_data import PredictiveMaintenanceJointData
from alliander_predictive_maintenance.conversion.partial_discharge_correlator.partial_discharge_weather_correlator_results import \
    PartialDischargeWeatherCorrelatorResults


class PartialDischargeWeatherCorrelator:
    """ A class for calculating correlations between partial discharge and weather data. """
    PARTIAL_DISCHARGE_COLUMN = "partial_discharge"

    def correlate(self, predictive_maintenance_joint_data: PredictiveMaintenanceJointData,
                  rolling_days: int) -> PartialDischargeWeatherCorrelatorResults:
        """ Calculate Pearson Correlation Coefficient for Partial Discharge data and weather data

        :param predictive_maintenance_joint_data: PredictiveMaintenanceJointData object
        :param rolling_days: number of days to use for a moving average
        :return: PartialDischargeWeatherCorrelatorResults
        """
        predictive_maintenance_joint_data.knmi_weather.drop(['lat', 'lon'], axis=1, inplace=True, errors='ignore')
        predictive_maintenance_joint_data.cds_weather.drop(['lat', 'lon', 'is_permanent_data', 'mean_wave_direction'],
                                                           axis=1, inplace=True,
                                                           errors='ignore')
        data_frame = predictive_maintenance_joint_data.cds_weather.set_index("time").join(
            predictive_maintenance_joint_data.partial_discharge.rename(self.PARTIAL_DISCHARGE_COLUMN))

        data_frame_resampled = data_frame.resample("1d").agg([np.sum, np.median, np.mean, np.min, np.max])
        data_frame_resampled['partial_discharge_cumsum'] = data_frame_resampled.partial_discharge['sum'].cumsum()
        data_frame_resampled['partial_discharge_cumsum_gradient'] = np.gradient(
            data_frame_resampled['partial_discharge_cumsum'])

        data_frame_resampled.columns = ['_'.join(col).strip('_') for col in data_frame_resampled.columns]
        data_frame_resampled = data_frame_resampled.join(
            predictive_maintenance_joint_data.knmi_weather.set_index("time"))

        data_frame_rolling = data_frame_resampled.rolling(rolling_days).mean()

        corr_matrix = data_frame_rolling.corr()
        corr_matrix.fillna(0, inplace=True)

        return PartialDischargeWeatherCorrelatorResults(corr_matrix)
