import pandas as pd
from dataclasses import dataclass


@dataclass
class Joint:
    location: float
    partial_discharge: pd.Series
