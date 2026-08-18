import pandas as pd
from olympics.components.data_loader import DataLoader
from olympics.components.preprocessor import OlympicPreprocessor
from olympics.components.medal_analyzer import MedalAnalyzer
from olympics.components.trend_analyzer import TrendAnalyzer
from olympics.components.country_analyzer import CountryAnalyzer
from olympics.components.demographic_analyzer import DemographicAnalyzer

class OlympicAnalyticsPipeline:
    def __init__(self, athlete_path: str = None, region_path: str = None, season: str = 'Summer'):
        self.data_loader = DataLoader(athlete_path, region_path)
        self.preprocessor = OlympicPreprocessor(season=season)
        self.df = self._initialize_data()
        
        self.medal_analyzer = MedalAnalyzer(self.df)
        self.trend_analyzer = TrendAnalyzer(self.df)
        self.country_analyzer = CountryAnalyzer(self.df)
        self.demographic_analyzer = DemographicAnalyzer(self.df)

    def _initialize_data(self) -> pd.DataFrame:
        athlete_df, region_df = self.data_loader.load_raw_data()
        return self.preprocessor.process(athlete_df, region_df)

    def get_summary_statistics(self) -> dict:
        return {
            'editions': self.df['Year'].nunique() - 1,
            'cities': self.df['City'].nunique(),
            'sports': self.df['Sport'].nunique(),
            'events': self.df['Event'].nunique(),
            'athletes': self.df['Name'].nunique(),
            'nations': self.df['region'].nunique(),
            'medals_awarded': self.df.dropna(subset=['Medal']).shape[0]
        }
