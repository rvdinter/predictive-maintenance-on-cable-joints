import abc

import pandas as pd


class IJointsWithPartialDischargeSeasonalityReader(metaclass=abc.ABCMeta):
    CIRCUIT_ID_COLUMN = "circuitnr"
    LOCATION_COLUMN = "Location in meters (m)"
    MANDATORY_COLUMNS = [CIRCUIT_ID_COLUMN, LOCATION_COLUMN]

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_joints_with_partial_discharge_seasonality') and
                callable(subclass.get_joints_with_partial_discharge_seasonality) or
                NotImplemented)

    @abc.abstractmethod
    def get_joints_with_partial_discharge_seasonality(self) -> pd.DataFrame:
        """Get a DataFrame of circuit ID and location combinations (a Joint) that
        show seasonality in partial discharge data"""
        raise NotImplementedError
