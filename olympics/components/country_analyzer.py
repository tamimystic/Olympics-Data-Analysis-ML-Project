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

    def get_country_sport_breakdown(self, country: str) -> pd.DataFrame:
        temp_df = self.df.dropna(subset=['Medal'])
        dedup = temp_df.drop_duplicates(
            subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal']
        )
        filtered = dedup[dedup['region'] == country]
        if filtered.empty:
            return pd.DataFrame(columns=['Sport', 'Gold', 'Silver', 'Bronze', 'Total'])
        summary = filtered.groupby('Sport').sum()[['Gold', 'Silver', 'Bronze']].reset_index()
        summary['Total'] = summary['Gold'] + summary['Silver'] + summary['Bronze']
        summary = summary.sort_values(by=['Gold', 'Total'], ascending=[False, False]).reset_index(drop=True)
        return summary

    def get_available_sports_for_country(self, country: str) -> list:
        temp_df = self.df.dropna(subset=['Medal'])
        filtered = temp_df[temp_df['region'] == country]
        sports = filtered['Sport'].dropna().unique().tolist()
        sports.sort()
        sports.insert(0, 'Overall')
        return sports

    def get_available_years_for_country(self, country: str) -> list:
        temp_df = self.df.dropna(subset=['Medal'])
        filtered = temp_df[temp_df['region'] == country]
        years = filtered['Year'].dropna().unique().tolist()
        years.sort(reverse=True)
        years.insert(0, 'All Years')
        return years

    def get_detailed_medalist_records(self, country: str, sport: str = 'Overall', medal_type: str = 'All Medals', year: str = 'All Years') -> pd.DataFrame:
        temp_df = self.df.dropna(subset=['Medal'])
        filtered = temp_df[temp_df['region'] == country]
        
        if sport != 'Overall':
            filtered = filtered[filtered['Sport'] == sport]
            
        if medal_type != 'All Medals':
            filtered = filtered[filtered['Medal'] == medal_type]
            
        if year != 'All Years':
            filtered = filtered[filtered['Year'] == int(year)]
            
        columns = ['Year', 'City', 'Sport', 'Event', 'Name', 'Medal', 'Sex', 'Age']
        result = filtered[columns].drop_duplicates().sort_values(by=['Year', 'Sport', 'Event'], ascending=[False, True, True]).reset_index(drop=True)
        result.rename(columns={'Name': 'Athlete Name'}, inplace=True)
        return result
