from enum import Enum


class PartialDischargeForecasterModel(Enum):
    """ An Enumeration to select the model type for forecasting Partial Discharge"""
    LASSO = 0
    SVR = 1
