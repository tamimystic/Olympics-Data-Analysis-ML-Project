import pandas as pd

class TrendAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_metrics_over_time(self, column_name: str) -> pd.DataFrame:
        data = self.df.drop_duplicates(['Year', column_name])['Year'].value_counts().reset_index()
        data.columns = ['Edition', column_name]
        data = data.sort_values('Edition')
        return data

    def get_sport_event_matrix(self) -> pd.DataFrame:
        unique_events = self.df.drop_duplicates(['Year', 'Sport', 'Event'])
        matrix = unique_events.pivot_table(
            index='Sport', columns='Year', values='Event', aggfunc='count'
        ).fillna(0).astype(int)
        return matrix

    def get_most_successful_athletes(self, sport: str = 'Overall', top_n: int = 15) -> pd.DataFrame:
        temp_df = self.df.dropna(subset=['Medal'])
        if sport != 'Overall':
            temp_df = temp_df[temp_df['Sport'] == sport]

        leaderboard = temp_df['Name'].value_counts().reset_index().head(top_n)
        leaderboard.columns = ['Name', 'Medals']
        merged = leaderboard.merge(self.df, on='Name', how='left')[
            ['Name', 'Medals', 'Sport', 'region']
        ].drop_duplicates('Name')
        return merged
