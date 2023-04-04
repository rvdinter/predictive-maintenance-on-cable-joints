import abc

import pandas as pd


class IFailedJointsReader(metaclass=abc.ABCMeta):
    DATETIME_COLUMN = "Date/time (UTC)"
    LOCATION_COLUMN = "Location in meters (m)"
    CIRCUIT_ID_COLUMN = "circuitnr"
    PRIORITY_COLUMN = "priority"
    LOCATION_FRACTIONAL_TIME_COLUMN = "locationFt"
    MANDATORY_COLUMNS = [DATETIME_COLUMN, LOCATION_COLUMN, CIRCUIT_ID_COLUMN, PRIORITY_COLUMN,
                         LOCATION_FRACTIONAL_TIME_COLUMN]

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_failed_joints_for_circuit') and
                callable(subclass.get_failed_joints_for_circuit) or
                NotImplemented)

    @abc.abstractmethod
    def get_failed_joints_for_circuit(self, circuit_id: int) -> pd.DataFrame:
        """Get a DataFrame of joint locations for a given circuit
        :param circuit_id: id of the circuit
        """
        raise NotImplementedError
