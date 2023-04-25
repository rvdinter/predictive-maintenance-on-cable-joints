import numpy as np
import pandas as pd
import pickle
from pathlib import Path
from skforecast.ForecasterAutoreg import ForecasterAutoreg
from sklearn.linear_model import Lasso
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVR
from typing import List, Dict

from alliander_predictive_maintenance.constants import INVALID_ENUM_INPUT, WEATHER_DATA_MANDATORY, \
    WEATHER_DATA_DATETIME_INDEX, PARTIAL_DISCHARGE_DATA_DATETIME_INDEX
from alliander_predictive_maintenance.conversion.data_types.predictive_maintenance_joint_data import \
    PredictiveMaintenanceJointData
from alliander_predictive_maintenance.cyber.simulation_model.partial_discharge_forecaster_model import \
    PartialDischargeForecasterModel
from alliander_predictive_maintenance.cyber.simulation_model.weather_and_partial_discharge_transformer import \
    WeatherAndPartialDischargeTransformer
from alliander_predictive_maintenance.cyber.simulation_model.partial_discharge_forecaster_model_results import PartialDischargeForecasterModelResults


class PartialDischargeForecaster:
    """ A model for forecasting Partial Discharge """
    WEATHER_COLUMNS = ["soil_temperature_level_3", "volumetric_soil_water_layer_3"]
    PARTIAL_DISCHARGE_COLUMN = "partial_discharge"

    def __init__(self, partial_discharge_forecaster_model: PartialDischargeForecasterModel, lags: List[int]):
        self.__partial_discharge_forecaster_model = partial_discharge_forecaster_model
        self.__lags = lags
        self.__forecaster = None
        self.__load_forecaster()
        self.__transformer = WeatherAndPartialDischargeTransformer(self.WEATHER_COLUMNS, self.PARTIAL_DISCHARGE_COLUMN)

    def fit(self, predictive_maintenance_joint_data: PredictiveMaintenanceJointData, train_size: float) -> \
            Dict[str, PartialDischargeForecasterModelResults]:
        """ Train the partial discharge forecasting model on historical data

        :param predictive_maintenance_joint_data: historical weather and partial discharge data. Must be of same length.
        :param train_size: ratio of training set. Usually 0.8 or 0.7.
        :return: model results dict for `train` and `test` keys
        """
        self.__check_input_data(predictive_maintenance_joint_data)
        enriched_predictive_maintenance_joint_data = self.__enrich_features(predictive_maintenance_joint_data)
        exog_train, exog_test, endog_train, endog_test = train_test_split(
            enriched_predictive_maintenance_joint_data.cds_weather, enriched_predictive_maintenance_joint_data.partial_discharge,
            train_size=train_size, shuffle=False)
        self.__forecaster.fit(y=endog_train, exog=exog_train)
        circuit_id = predictive_maintenance_joint_data.circuit_id
        location_in_meters = predictive_maintenance_joint_data.location_in_meters
        predictive_maintenance_joint_data_train = PredictiveMaintenanceJointData(cds_weather=exog_train,
                                                                                 knmi_weather=None,
                                                                                 partial_discharge=endog_train,
                                                                                 circuit_id=circuit_id,
                                                                                 location_in_meters=location_in_meters)
        predictive_maintenance_joint_data_test = PredictiveMaintenanceJointData(cds_weather=exog_test,
                                                                                knmi_weather=None,
                                                                                partial_discharge=endog_test,
                                                                                circuit_id=circuit_id,
                                                                                location_in_meters=location_in_meters)
        return self.__validate_train(predictive_maintenance_joint_data_train, predictive_maintenance_joint_data_test)

    def predict(self, predictive_maintenance_joint_data: PredictiveMaintenanceJointData) -> \
            PartialDischargeForecasterModelResults:
        """ Predict partial discharge on historical data

        :param predictive_maintenance_joint_data: historical weather and partial discharge data. Must be of same length.
        :return: model results
        """
        self.__check_input_data(predictive_maintenance_joint_data)
        enriched_predictive_maintenance_joint_data = self.__enrich_features(predictive_maintenance_joint_data)
        predictions = self.__forecaster.predict(steps=len(enriched_predictive_maintenance_joint_data.cds_weather),
                                                exog=enriched_predictive_maintenance_joint_data.cds_weather)
        predictions[predictions < 0] = 0
        score = r2_score(enriched_predictive_maintenance_joint_data.partial_discharge, predictions)
        return PartialDischargeForecasterModelResults(
            predictions, enriched_predictive_maintenance_joint_data.partial_discharge, score)

    def save_weights(self, absolute_path: Path):
        """ Save the model weights
        :param absolute_path: path of model parameters
        """
        pickle.dump(self.__forecaster,
                    open(absolute_path / f"{self.__partial_discharge_forecaster_model}.pickle", 'wb'))

    def load_weights(self, absolute_path: Path):
        """ Load the model weights
        :param absolute_path: path of model parameters
        """
        self.__forecaster = pickle.load(
            open(absolute_path / f"{self.__partial_discharge_forecaster_model}.pickle", 'rb'))

    def __check_input_data(self, predictive_maintenance_joint_data: PredictiveMaintenanceJointData):
        """ Check the input data
        :param predictive_maintenance_joint_data: input data
        """
        if not all([column in predictive_maintenance_joint_data.cds_weather.columns for column in self.WEATHER_COLUMNS]):
            raise ValueError(WEATHER_DATA_MANDATORY.format(
                data=predictive_maintenance_joint_data.cds_weather.columns, mandatory=self.WEATHER_COLUMNS))
        if not isinstance(predictive_maintenance_joint_data.cds_weather.index, pd.DatetimeIndex):
            raise ValueError(WEATHER_DATA_DATETIME_INDEX)
        if not isinstance(predictive_maintenance_joint_data.partial_discharge.index, pd.DatetimeIndex):
            raise ValueError(PARTIAL_DISCHARGE_DATA_DATETIME_INDEX)

    def __enrich_features(self, predictive_maintenance_joint_data: PredictiveMaintenanceJointData) -> \
            PredictiveMaintenanceJointData:
        """ Enrich the input features for the model

        :param predictive_maintenance_joint_data: historical weather and partial discharge data. Must be of same length.
        :return: enriched data
        """
        return self.__transformer.transform(
            predictive_maintenance_joint_data, lags=self.__lags, methods=[np.mean, np.std, np.min, np.max])

    def __validate_train(self,
                         predictive_maintenance_joint_data_train: PredictiveMaintenanceJointData,
                         predictive_maintenance_joint_data_test: PredictiveMaintenanceJointData) -> \
            Dict[str, PartialDischargeForecasterModelResults]:
        """ Validate the training set

        :param predictive_maintenance_joint_data_train: train data
        :param predictive_maintenance_joint_data_test: test data
        :return: model results dict for `train` and `test` keys
        """
        X_train, _ = self.__forecaster.create_train_X_y(y=predictive_maintenance_joint_data_train.partial_discharge,
                                                        exog=predictive_maintenance_joint_data_train.cds_weather)
        train_endog = predictive_maintenance_joint_data_train.partial_discharge[X_train.index.min():X_train.index.max()]
        train_predictions = self.__forecaster.regressor.predict(X_train)
        test_predictions = self.__forecaster.predict(steps=len(predictive_maintenance_joint_data_test.partial_discharge),
                                                     exog=predictive_maintenance_joint_data_test.cds_weather)
        result = {}
        for type, predictions, endog in [("train", train_predictions, train_endog),
                                         ("test", test_predictions, predictive_maintenance_joint_data_test.partial_discharge)]:
            predictions[predictions < 0] = 0
            r2 = r2_score(endog, predictions)
            result[type] = PartialDischargeForecasterModelResults(predictions, endog, r2)
        return result

    def __load_forecaster(self):
        """ Load the correct forecaster depending on the __partial_discharge_forecaster_model attribute """
        if self.__partial_discharge_forecaster_model == PartialDischargeForecasterModel.SVR:
            self.__forecaster = ForecasterAutoreg(regressor=LinearSVR(random_state=0), lags=1)
        elif self.__partial_discharge_forecaster_model == PartialDischargeForecasterModel.LASSO:
            self.__forecaster = ForecasterAutoreg(regressor=Lasso(random_state=0), lags=1)
        else:
            raise ValueError(f"{INVALID_ENUM_INPUT}: {self.__partial_discharge_forecaster_model}")
