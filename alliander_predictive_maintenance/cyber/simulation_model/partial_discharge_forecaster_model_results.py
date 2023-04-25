from dataclasses import dataclass

import pandas as pd


@dataclass
class PartialDischargeForecasterModelResults:
    partial_discharge: pd.Series
    true_partial_discharge: pd.Series
    r2_score: float