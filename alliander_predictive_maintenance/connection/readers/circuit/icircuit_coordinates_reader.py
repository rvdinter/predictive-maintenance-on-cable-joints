import abc

from alliander_predictive_maintenance.conversion.data_types.circuit_coordinate import CircuitCoordinate


class ICircuitCoordinatesReader(metaclass=abc.ABCMeta):
    X_COORDINATE_COLUMN = "x_coordinate"
    Y_COORDINATE_COLUMN = "y_coordinate"
    CIRCUIT_ID_COLUMN = "circuit_nr"
    DATE_SAVED_COLUMN = "date_saved"
    CIRCUIT_COORDINATES_COLUMN = "circuit_coordinates"
    MANDATORY_COLUMNS = [X_COORDINATE_COLUMN, Y_COORDINATE_COLUMN, CIRCUIT_ID_COLUMN, DATE_SAVED_COLUMN]

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_circuit_coordinate') and
                callable(subclass.get_circuit_coordinate) or
                NotImplemented)

    @abc.abstractmethod
    def get_circuit_coordinate(self, circuit_id: int) -> CircuitCoordinate:
        """Get a CircuitCoordinate of a given circuit
        :param circuit_id: id of the circuit
        """
        raise NotImplementedError
