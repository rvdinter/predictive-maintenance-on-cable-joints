import abc

import pandas as pd


class ICircuitPartialDischargeReader(metaclass=abc.ABCMeta):
    DATETIME_COLUMN = "Date/time (UTC)"
    PARTIAL_DISCHARGE_DATA_COLUMN = "Charge (picocoulomb)"
    LOCATION_COLUMN = "Location in meters (m)"
    MANDATORY_COLUMNS = [DATETIME_COLUMN, PARTIAL_DISCHARGE_DATA_COLUMN, LOCATION_COLUMN]

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_partial_discharge_data_for_circuit') and
                callable(subclass.get_partial_discharge_data_for_circuit) or
                NotImplemented)

    @abc.abstractmethod
    def get_partial_discharge_data_for_circuit(self, circuit_id: str) -> pd.DataFrame:
        """Get the partial discharge data for the loaded circuit

        :param circuit_id: the circuit id to load
        """
        raise NotImplementedError
