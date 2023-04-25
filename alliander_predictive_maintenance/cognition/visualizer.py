import matplotlib.pyplot as plt
import seaborn as sns

from alliander_predictive_maintenance.conversion.partial_discharge_correlator.partial_discharge_weather_correlator_results import \
    PartialDischargeWeatherCorrelatorResults
from alliander_predictive_maintenance.conversion.partial_discharge_correlator.weather_categories import WeatherCategories
from alliander_predictive_maintenance.cyber.simulation_model.partial_discharge_forecaster_model_results import PartialDischargeForecasterModelResults


class Visualizer:
    """ A class for visualizing results of several models. """

    def plot_forecasted_partial_discharge(self, results: PartialDischargeForecasterModelResults, axes: plt.Axes,
                                          title: str, ylabel: str, xlabel: str):
        """ Plot PartialDischargeForecasterModelResults

        :param results: PartialDischargeForecasterModelResults
        :param axes: axes for subplots
        :param title: title of the subplot
        :param ylabel: y label of the subplot
        :param xlabel: x label of the subplot
        """
        self.__plot_partial_discharge_forecaster_model_results(results, "ground truth", "predictions", "red", axes)
        self.__set_title_and_labels(axes, title, ylabel, xlabel)

    def plot_forecasted_train_partial_discharge(self, train_results: PartialDischargeForecasterModelResults,
                                                test_results: PartialDischargeForecasterModelResults,
                                                axes: plt.Axes, title: str, ylabel: str, xlabel: str):
        """ Plot PartialDischargeForecasterModelResults for after fitting the model

        :param train_results: PartialDischargeForecasterModelResults for the train set
        :param test_results: PartialDischargeForecasterModelResults for the test set
        :param axes: axes for subplots
        :param title: title of the subplot
        :param ylabel: y label of the subplot
        :param xlabel: x label of the subplot
        """
        self.__plot_partial_discharge_forecaster_model_results(train_results, "train", "train predictions", "green",
                                                               axes)
        self.__plot_partial_discharge_forecaster_model_results(test_results, "test", "test predictions", "red", axes)
        self.__set_title_and_labels(axes, title, ylabel, xlabel)

    def __plot_partial_discharge_forecaster_model_results(self, results: PartialDischargeForecasterModelResults,
                                                          ground_truth_label: str, predict_label: str, color: str,
                                                          axes: plt.Axes):
        """ Plot partial discharge forecaster model results

        :param results: PartialDischargeForecasterModelResults
        :param ground_truth_label: string for legend
        :param predict_label: string for legend
        :param color: color of predicted values
        :param axes: axes for subplot
        """
        axes.plot(results.true_partial_discharge, label=ground_truth_label)
        axes.plot(results.true_partial_discharge.index, results.partial_discharge, label=predict_label, c=color)

    def __set_title_and_labels(self, axes: plt.Axes, title: str, ylabel: str, xlabel: str):
        """ Set title and labels of subplots

        :param axes: axes for subplots
        :param title: title of the subplot
        :param ylabel: y label of the subplot
        :param xlabel: x label of the subplot
        """
        axes.set_title(title)
        axes.set_ylabel(ylabel)
        axes.set_xlabel(xlabel)
        axes.legend()

    def plot_partial_discharge_weather_correlation(self, correlator_results: PartialDischargeWeatherCorrelatorResults,
                                                   axes: plt.Axes, title: str, ylabel: str, xlabel: str,
                                                   correlation_coefficient_threshold: float):
        """ Plot model results of the PartialDischargeWeatherCorrelator

        :param correlator_results: PartialDischargeWeatherCorrelatorResults
        :param axes: axes for subplots
        :param title: title of the subplot
        :param ylabel: y label of the subplot
        :param xlabel: x label of the subplot
        :param correlation_coefficient_threshold: threshold for Pearson correlation coefficient
        """
        for weather_category in WeatherCategories:
            correlating_features = correlator_results.partial_discharge_correlating_weather_features(
                weather_category, correlation_coefficient_threshold)
            if len(correlating_features) > 0:
                print(f"Correlates with {weather_category.name}: {correlating_features[-1]:.2f} for feature "
                      f"{correlating_features.index[-1][1]}")

        # plot a heatmap of pd features vs weather features
        corr = correlator_results.correlations
        pd_columns = [column for column in corr.columns if 'partial_discharge' in column]
        corr_filtered = corr[~corr.index.isin(pd_columns)]
        corr_filtered = corr_filtered[pd_columns]
        significant_features = corr_filtered.apply(lambda row: any(row.abs() > correlation_coefficient_threshold),
                                                   axis=1)
        corr_filtered = corr_filtered.loc[significant_features[significant_features].index]
        sns.heatmap(corr_filtered, annot=True, cmap=plt.cm.PuBu, ax=axes)
        self.__set_title_and_labels(axes, title, ylabel, xlabel)
