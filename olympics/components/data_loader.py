import os
import pandas as pd
from typing import Tuple

class DataLoader:
    def __init__(self, athlete_file_path: str = None, region_file_path: str = None):
        self.athlete_file_path = athlete_file_path or self._resolve_athlete_path()
        self.region_file_path = region_file_path or self._resolve_region_path()

    def _resolve_athlete_path(self) -> str:
        candidates = [
            "Olympic Analysis/athlete_events.csv",
            "athlete_events.csv",
            "data/athlete_events.csv"
        ]
        for path in candidates:
            if os.path.exists(path):
                return path
        raise FileNotFoundError("athlete_events.csv not found in candidate paths.")

    def _resolve_region_path(self) -> str:
        candidates = [
            "Olympic Analysis/noc_regions.csv",
            "noc_regions.csv",
            "data/noc_regions.csv"
        ]
        for path in candidates:
            if os.path.exists(path):
                return path
        raise FileNotFoundError("noc_regions.csv not found in candidate paths.")

    def load_raw_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        athlete_df = pd.read_csv(self.athlete_file_path)
        region_df = pd.read_csv(self.region_file_path)
        return athlete_df, region_df
