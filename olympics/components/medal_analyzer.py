import numpy as np
import pandas as pd
from typing import Tuple

class MedalAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.medal_df = df.drop_duplicates(
            subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal']
        )

    def get_filter_options(self) -> Tuple[list, list]:
        years = self.df['Year'].unique().tolist()
        years.sort()
        years.insert(0, 'Overall')

        countries = np.unique(self.df['region'].dropna().values).tolist()
        countries.sort()
        countries.insert(0, 'Overall')

        return years, countries

    def calculate_medal_tally(self, year: str = 'Overall', country: str = 'Overall') -> pd.DataFrame:
        flag = 0
        if year == 'Overall' and country == 'Overall':
            temp_df = self.medal_df
        elif year == 'Overall' and country != 'Overall':
            flag = 1
            temp_df = self.medal_df[self.medal_df['region'] == country]
        elif year != 'Overall' and country == 'Overall':
            temp_df = self.medal_df[self.medal_df['Year'] == int(year)]
        elif year != 'Overall' and country != 'Overall':
            temp_df = self.medal_df[
                (self.medal_df['Year'] == int(year)) & (self.medal_df['region'] == country)
            ]

        if flag == 1:
            result = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
        else:
            result = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

        result['total'] = result['Gold'] + result['Silver'] + result['Bronze']
        return result
