import pandas as pd
from dataclasses import dataclass
from typing import Union, Optional


@dataclass
class PredictiveMaintenanceJointData:
    """ Data needed for predictive maintenance on a cable joint.
    weather: historical weather data. partial_discharge: historical partial discharge data."""
    cds_weather: pd.DataFrame
    knmi_weather: Optional[pd.DataFrame]
    partial_discharge: Union[pd.DataFrame, pd.Series]
    circuit_id: int
    location_in_meters: float
