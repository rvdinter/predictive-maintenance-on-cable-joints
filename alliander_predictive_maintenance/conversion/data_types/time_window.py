from dataclasses import dataclass

import pandas as pd


@dataclass
class TimeWindow:
    start_date: pd.Timestamp
    end_date: pd.Timestamp
