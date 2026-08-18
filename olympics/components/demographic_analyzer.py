import pandas as pd

class DemographicAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.unique_athletes = df.drop_duplicates(subset=['Name', 'region'])

    def get_age_distributions(self):
        overall_age = self.unique_athletes['Age'].dropna()
        gold_age = self.unique_athletes[self.unique_athletes['Medal'] == 'Gold']['Age'].dropna()
        silver_age = self.unique_athletes[self.unique_athletes['Medal'] == 'Silver']['Age'].dropna()
        bronze_age = self.unique_athletes[self.unique_athletes['Medal'] == 'Bronze']['Age'].dropna()
        return overall_age, gold_age, silver_age, bronze_age

    def get_physical_data_by_sport(self, sport: str = 'Overall') -> pd.DataFrame:
        data = self.unique_athletes.copy()
        data['Medal'] = data['Medal'].fillna('No Medal')
        if sport != 'Overall':
            data = data[data['Sport'] == sport]
        return data

    def get_gender_participation_history(self) -> pd.DataFrame:
        male_counts = self.unique_athletes[self.unique_athletes['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
        female_counts = self.unique_athletes[self.unique_athletes['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
        merged = male_counts.merge(female_counts, on='Year', how='left')
        merged.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
        merged.fillna(0, inplace=True)
        return merged
