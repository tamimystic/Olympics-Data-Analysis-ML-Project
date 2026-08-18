import pandas as pd

class OlympicPreprocessor:
    def __init__(self, season: str = 'Summer'):
        self.season = season

    def process(self, athlete_df: pd.DataFrame, region_df: pd.DataFrame) -> pd.DataFrame:
        df = athlete_df.copy()
        if self.season:
            df = df[df['Season'] == self.season]

        df = df.merge(region_df, on='NOC', how='left')
        df['region'] = df['region'].fillna(df['Team'])
        df.drop_duplicates(inplace=True)

        dummies = pd.get_dummies(df['Medal'], dtype=int)
        df = pd.concat([df, dummies], axis=1)

        for medal_type in ['Gold', 'Silver', 'Bronze']:
            if medal_type not in df.columns:
                df[medal_type] = 0

        return df
