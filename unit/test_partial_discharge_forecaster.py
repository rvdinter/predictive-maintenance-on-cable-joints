import math

import numpy as np
import pandas as pd
import pytest

from alliander_predictive_maintenance.cognition.visualizer import Visualizer
from alliander_predictive_maintenance.cyber.simulation_model.partial_discharge_forecaster import \
    PartialDischargeForecaster
from alliander_predictive_maintenance.cyber.simulation_model.partial_discharge_forecaster_model import \
    PartialDischargeForecasterModel


@pytest.fixture
def tmp_weather_partial_discharge_data():
    n_samples = 10000
    x = np.linspace(0, n_samples, n_samples)
    datetime = pd.date_range(start='1/1/2018', periods=n_samples)
    weather = pd.DataFrame(np.column_stack((2 * x, 3 * x)), columns=PartialDischargeForecaster.WEATHER_COLUMNS,
                           index=datetime)
    partial_discharge = pd.Series(2 * x, name=PartialDischargeForecaster.PARTIAL_DISCHARGE_COLUMN, index=datetime)
    return weather, partial_discharge


class TestPartialDischargeForecaster:
    @pytest.mark.parametrize("partial_discharge_forecaster_model",
                             [PartialDischargeForecasterModel.SVR, PartialDischargeForecasterModel.LASSO])
    def test_train__valid_input__trained_model_score_returned(self, partial_discharge_forecaster_model,
                                                              tmp_weather_partial_discharge_data):
        visualizer = Visualizer()
        partial_discharge_forecaster = PartialDischargeForecaster(partial_discharge_forecaster_model, [7], visualizer)
        weather, partial_discharge = tmp_weather_partial_discharge_data
        score = partial_discharge_forecaster.train(weather, partial_discharge, train_size=0.7)
        assert math.isclose(score["r2_train"], 1, abs_tol=0.00001)
        assert math.isclose(score["r2_test"], 1, abs_tol=0.00001)

    @pytest.mark.parametrize("partial_discharge_forecaster_model",
                             [PartialDischargeForecasterModel.SVR, PartialDischargeForecasterModel.LASSO])
    def test_train__invalid_input__exception_thrown(self, partial_discharge_forecaster_model,
                                                    tmp_weather_partial_discharge_data):
        visualizer = Visualizer()
        partial_discharge_forecaster = PartialDischargeForecaster(partial_discharge_forecaster_model, [7], visualizer)
        weather, partial_discharge = tmp_weather_partial_discharge_data
        with pytest.raises(ValueError):
            partial_discharge_forecaster.train(weather.reset_index(drop=True), partial_discharge, train_size=0.7)
        with pytest.raises(ValueError):
            partial_discharge_forecaster.train(weather, partial_discharge.reset_index(drop=True), train_size=0.7)
        with pytest.raises(ValueError):
            partial_discharge_forecaster.train(weather.add_suffix("_invalid"), partial_discharge, train_size=0.7)

    @pytest.mark.parametrize("partial_discharge_forecaster_model",
                             [PartialDischargeForecasterModel.SVR, PartialDischargeForecasterModel.LASSO])
    def test_predict__valid_input__predictions_returned(self, partial_discharge_forecaster_model,
                                                        tmp_weather_partial_discharge_data):
        visualizer = Visualizer()
        partial_discharge_forecaster = PartialDischargeForecaster(partial_discharge_forecaster_model, [7], visualizer)
        weather, partial_discharge = tmp_weather_partial_discharge_data

        n_train = 1000
        weather_train = weather[:n_train]
        weather_val = weather[n_train:]
        partial_discharge_train = partial_discharge[:n_train]
        partial_discharge_val = partial_discharge[n_train:]
        partial_discharge_forecaster.train(weather_train, partial_discharge_train, train_size=0.7)
        _, _, score = partial_discharge_forecaster.predict(weather_val, partial_discharge_val)
        assert math.isclose(score, 1, abs_tol=0.03)

        intercept = 10
        _, _, score = partial_discharge_forecaster.predict(weather_val + intercept, partial_discharge_val + intercept)
        assert math.isclose(score, 1, abs_tol=0.03)

    @pytest.mark.parametrize("partial_discharge_forecaster_model",
                             [PartialDischargeForecasterModel.SVR, PartialDischargeForecasterModel.LASSO])
    def test_predict__valid_nonlinear_input__high_error_returned(self, partial_discharge_forecaster_model,
                                                                 tmp_weather_partial_discharge_data):
        visualizer = Visualizer()
        partial_discharge_forecaster = PartialDischargeForecaster(partial_discharge_forecaster_model, [7], visualizer)
        weather, partial_discharge = tmp_weather_partial_discharge_data

        n_train = 1000
        weather_train = weather[:n_train]
        weather_val = weather[n_train:]
        partial_discharge_train = partial_discharge[:n_train]
        partial_discharge_val = partial_discharge[n_train:]
        partial_discharge_forecaster.train(weather_train, partial_discharge_train, train_size=0.7)
        _, _, score = partial_discharge_forecaster.predict(weather_val, partial_discharge_val)
        assert math.isclose(score, 1, abs_tol=0.03)

        intercept = 10
        weight = 10
        _, _, score = partial_discharge_forecaster.predict((weather_val + intercept) ** weight,
                                                           (partial_discharge_val + intercept) ** weight)
        assert not math.isclose(score, 1, abs_tol=0.03)

    @pytest.mark.parametrize("partial_discharge_forecaster_model",
                             [PartialDischargeForecasterModel.SVR, PartialDischargeForecasterModel.LASSO])
    def test_predict__invalid_input__exception_thrown(self, partial_discharge_forecaster_model,
                                                      tmp_weather_partial_discharge_data):
        visualizer = Visualizer()
        partial_discharge_forecaster = PartialDischargeForecaster(partial_discharge_forecaster_model, [7], visualizer)
        weather, partial_discharge = tmp_weather_partial_discharge_data
        partial_discharge_forecaster.train(weather, partial_discharge, train_size=0.7)

        with pytest.raises(ValueError):
            partial_discharge_forecaster.predict(weather.reset_index(drop=True), partial_discharge)
        with pytest.raises(ValueError):
            partial_discharge_forecaster.predict(weather, partial_discharge.reset_index(drop=True))
        with pytest.raises(ValueError):
            partial_discharge_forecaster.predict(weather.add_suffix("_invalid"), partial_discharge)
