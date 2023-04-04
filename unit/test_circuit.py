import numpy as np
import pandas as pd
import pytest

from alliander_predictive_maintenance.conversion.circuit import Circuit
from alliander_predictive_maintenance.connection.circuit_coordinate import CircuitCoordinate
from alliander_predictive_maintenance.connection.icircuit_partial_discharge_reader import ICircuitPartialDischargeReader
from alliander_predictive_maintenance.conversion.time_window import TimeWindow


class TestCircuit:
    LOCATION = 150
    CIRCUIT_LENGTH = 1500
    NUMBER_OP_PARTIAL_DISCHARGES_ON_LOCATION = 30
    MARGIN = pd.Timedelta(5, "W")
    CIRCUIT_COORDINATE = CircuitCoordinate(52.508969, 4.986738, 23108)
    JOINT_TIME_WINDOW = TimeWindow(pd.Timestamp("01/01/2019"), pd.Timestamp("01/20/2019"))
    CIRCUIT_TIME_WINDOW = TimeWindow(JOINT_TIME_WINDOW.start_date - MARGIN, JOINT_TIME_WINDOW.end_date + MARGIN)

    def test_create_joint__valid_location__joint_returned(self):
        circuit = self.__get_circuit()
        joint = circuit.create_joint(self.LOCATION, self.JOINT_TIME_WINDOW)
        assert np.count_nonzero(joint.partial_discharge) == self.NUMBER_OP_PARTIAL_DISCHARGES_ON_LOCATION - 1

    def test_create_joint__invalid_location__exception_thrown(self):
        circuit = self.__get_circuit()
        with pytest.raises(ValueError):
            circuit.create_joint(self.CIRCUIT_LENGTH + 15, self.JOINT_TIME_WINDOW)

    def test_create_joint__invalid_time_window__exception_thrown(self):
        circuit = self.__get_circuit()
        with pytest.raises(ValueError):
            circuit.create_joint(self.CIRCUIT_LENGTH, self.CIRCUIT_TIME_WINDOW)

    def __get_circuit(self):
        np.random.seed(42)
        weather_index = pd.date_range(self.CIRCUIT_TIME_WINDOW.start_date,
                                      self.CIRCUIT_TIME_WINDOW.end_date, freq="1H")
        weather_data = np.random.random(len(weather_index))
        weather = pd.DataFrame({"temperature": weather_data, "rain": weather_data}, weather_index)

        partial_discharge_datetime = pd.date_range(self.JOINT_TIME_WINDOW.start_date, self.JOINT_TIME_WINDOW.end_date,
                                                   freq="1H")
        partial_discharge_location = np.full(len(partial_discharge_datetime), 20)
        random_indices = np.random.choice(len(partial_discharge_location),
                                          size=self.NUMBER_OP_PARTIAL_DISCHARGES_ON_LOCATION)
        partial_discharge_location[random_indices] = self.LOCATION
        partial_discharge_data = np.random.random(len(partial_discharge_datetime))
        partial_discharge = pd.DataFrame(
            {ICircuitPartialDischargeReader.PARTIAL_DISCHARGE_DATA_COLUMN: partial_discharge_data,
             ICircuitPartialDischargeReader.LOCATION_COLUMN: partial_discharge_location,
             ICircuitPartialDischargeReader.DATETIME_COLUMN: partial_discharge_datetime})

        circuit = Circuit(circuit_id=1234, weather=weather, circuit_coordinate=self.CIRCUIT_COORDINATE,
                          partial_discharge=partial_discharge, circuit_length=self.CIRCUIT_LENGTH,
                          time_window=self.CIRCUIT_TIME_WINDOW)
        return circuit
