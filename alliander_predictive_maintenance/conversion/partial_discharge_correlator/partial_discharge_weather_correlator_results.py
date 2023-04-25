import pandas as pd
from dataclasses import dataclass

from alliander_predictive_maintenance.conversion.partial_discharge_correlator.weather_categories import WeatherCategories


@dataclass
class PartialDischargeWeatherCorrelatorResults:
    """ A data class that contains partial discharge and weather correlation results. """
    correlations: pd.Series

    @property
    def sorted_correlation_series(self) -> pd.Series:
        """ A property returning a sorted series of correlations.
        The first level of MultiIndex is partial_discharge-related, the second level is weather-related."""
        corr_matrix_unstacked = self.correlations.unstack()
        sorted_corr_series = corr_matrix_unstacked.sort_values(key=abs)

        pd_columns = [column for column in self.correlations.columns if 'partial_discharge' in column]

        sorted_corr_series = sorted_corr_series[sorted_corr_series.index.get_level_values(0) !=
                                                sorted_corr_series.index.get_level_values(1)]
        sorted_corr_series = sorted_corr_series[sorted_corr_series.index.get_level_values(0).isin(pd_columns)]
        sorted_corr_series = sorted_corr_series[~sorted_corr_series.index.get_level_values(1).isin(pd_columns)]
        return sorted_corr_series

    def partial_discharge_correlating_weather_features(self, weather_category: WeatherCategories,
                                                       correlation_coefficient_threshold: float) -> pd.Series:
        """ Find weather features in a weather category that correlate with partial discharge
        :param weather_category: WeatherCategories attribute
        :param correlation_coefficient_threshold: Pearson Correlation Coefficient threshold
        :return: series of correlations over the threshold for a specific weather category
        """
        sorted_corr_series = self.sorted_correlation_series.copy()
        sorted_corr_series = sorted_corr_series[sorted_corr_series > correlation_coefficient_threshold]
        sorted_corr_series = sorted_corr_series[
            sorted_corr_series.index.get_level_values(1).isin(weather_category.value)]
        return sorted_corr_series
