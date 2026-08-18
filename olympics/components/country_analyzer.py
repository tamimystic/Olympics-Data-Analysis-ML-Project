import pandas as pd

class CountryAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_country_list(self) -> list:
        countries = self.df['region'].dropna().unique().tolist()
        countries.sort()
        return countries

    def get_country_medal_trajectory(self, country: str) -> pd.DataFrame:
        temp_df = self.df.dropna(subset=['Medal'])
        temp_df = temp_df.drop_duplicates(
            subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal']
        )
        filtered = temp_df[temp_df['region'] == country]
        if filtered.empty:
            return pd.DataFrame(columns=['Year', 'Medal'])
        trajectory = filtered.groupby('Year').count()['Medal'].reset_index()
        return trajectory

    def get_country_sport_heatmap(self, country: str) -> pd.DataFrame:
        temp_df = self.df.dropna(subset=['Medal'])
        temp_df = temp_df.drop_duplicates(
            subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal']
        )
        filtered = temp_df[temp_df['region'] == country]
        if filtered.empty:
            return pd.DataFrame()
        matrix = filtered.pivot_table(
            index='Sport', columns='Year', values='Medal', aggfunc='count'
        ).fillna(0)
        return matrix

    def get_top_country_athletes(self, country: str, top_n: int = 10) -> pd.DataFrame:
        temp_df = self.df.dropna(subset=['Medal'])
        filtered = temp_df[temp_df['region'] == country]
        if filtered.empty:
            return pd.DataFrame(columns=['Name', 'Medals', 'Sport'])
        ranked = filtered['Name'].value_counts().reset_index().head(top_n)
        ranked.columns = ['Name', 'Medals']
        merged = ranked.merge(self.df, on='Name', how='left')[
            ['Name', 'Medals', 'Sport']
        ].drop_duplicates('Name')
        return merged
