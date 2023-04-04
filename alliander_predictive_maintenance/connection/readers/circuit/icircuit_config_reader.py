import abc

import pandas as pd


class ICircuitConfigReader(metaclass=abc.ABCMeta):
    COMPONENT_TYPE_COLUMN = "Component type"
    LENGTH_COLUMN = "Length (m)"
    CUMULATIVE_LENGTH_COLUMN = "Cumulative length (m)"
    COMPONENT_NAME_COLUMN = "Name"
    DISTANCE_TO_START_COLUMN = "Distance to start (m)"
    DISTANCE_TO_END_COLUMN = "Distance to end (m)"
    MANDATORY_COLUMNS = [COMPONENT_TYPE_COLUMN, LENGTH_COLUMN, DISTANCE_TO_START_COLUMN, DISTANCE_TO_END_COLUMN,
                         CUMULATIVE_LENGTH_COLUMN, COMPONENT_NAME_COLUMN]

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_circuit_config') and
                callable(subclass.get_circuit_config) or
                NotImplemented)

    @abc.abstractmethod
    def get_circuit_config(self, circuit_id: str) -> pd.DataFrame:
        """Get the config data for the loaded circuit

        :param circuit_id: the circuit id to load
        """
        raise NotImplementedError
