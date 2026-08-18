import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pandas as pd

class ChartBuilder:
    @staticmethod
    def create_choropleth_map(data: pd.DataFrame) -> go.Figure:
        fig = px.choropleth(
            data,
            locations="region",
            locationmode="country names",
            color="total",
            hover_name="region",
            hover_data={"Gold": True, "Silver": True, "Bronze": True, "total": True, "region": False},
            color_continuous_scale="Plasma"
        )
        fig.update_layout(
            height=320,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            geo=dict(
                showland=True,
                landcolor='#161b22',
                showocean=True,
                oceancolor='#0d1117',
                showcountries=True,
                countrycolor='#30363d',
                bgcolor='#0d1117',
                projection_type='natural earth'
            ),
            coloraxis_colorbar=dict(title="Medals")
        )
        return fig

    @staticmethod
    def create_stacked_medal_bar(data: pd.DataFrame) -> go.Figure:
        top_data = data.head(10)
        fig = go.Figure()
        fig.add_trace(go.Bar(y=top_data['region'], x=top_data['Gold'], name='Gold', orientation='h', marker_color='#d29922'))
        fig.add_trace(go.Bar(y=top_data['region'], x=top_data['Silver'], name='Silver', orientation='h', marker_color='#94a3b8'))
        fig.add_trace(go.Bar(y=top_data['region'], x=top_data['Bronze'], name='Bronze', orientation='h', marker_color='#b45309'))
        fig.update_layout(
            barmode='stack',
            height=320,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#8b949e', size=11),
            yaxis=dict(autorange="reversed"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        return fig

    @staticmethod
    def create_sport_breakdown_bar(data: pd.DataFrame) -> go.Figure:
        top_data = data.head(12)
        fig = go.Figure()
        fig.add_trace(go.Bar(y=top_data['Sport'], x=top_data['Gold'], name='Gold', orientation='h', marker_color='#d29922'))
        fig.add_trace(go.Bar(y=top_data['Sport'], x=top_data['Silver'], name='Silver', orientation='h', marker_color='#94a3b8'))
        fig.add_trace(go.Bar(y=top_data['Sport'], x=top_data['Bronze'], name='Bronze', orientation='h', marker_color='#b45309'))
        fig.update_layout(
            barmode='stack',
            height=340,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#8b949e', size=11),
            yaxis=dict(autorange="reversed"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        return fig

    @staticmethod
    def create_line_chart(data: pd.DataFrame, x_col: str, y_col: str, line_color: str = '#58a6ff') -> go.Figure:
        fig = px.line(data, x=x_col, y=y_col, markers=True)
        fig.update_traces(line_color=line_color, line_width=3)
        fig.update_layout(
            height=280,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#8b949e'),
            xaxis=dict(showgrid=True, gridcolor='#21262d'),
            yaxis=dict(showgrid=True, gridcolor='#21262d')
        )
        return fig

    @staticmethod
    def create_heatmap(matrix: pd.DataFrame, color_scale: str = "Viridis", height: int = 450) -> go.Figure:
        fig = px.imshow(matrix, color_continuous_scale=color_scale, aspect="auto")
        fig.update_layout(
            height=height,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#8b949e', size=10)
        )
        return fig

    @staticmethod
    def create_age_distribution_plot(overall_age, gold_age, silver_age, bronze_age) -> go.Figure:
        fig = ff.create_distplot(
            [overall_age, gold_age, silver_age, bronze_age],
            ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
            show_hist=False,
            show_rug=False,
            colors=['#58a6ff', '#d29922', '#94a3b8', '#b45309']
        )
        fig.update_layout(
            height=320,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#8b949e'),
            xaxis=dict(showgrid=True, gridcolor='#21262d', title="Age"),
            yaxis=dict(showgrid=True, gridcolor='#21262d')
        )
        return fig

    @staticmethod
    def create_scatter_plot(data: pd.DataFrame) -> go.Figure:
        fig = px.scatter(
            data,
            x="Weight",
            y="Height",
            color="Medal",
            symbol="Sex",
            color_discrete_map={'Gold': '#d29922', 'Silver': '#94a3b8', 'Bronze': '#b45309', 'No Medal': '#30363d'},
            opacity=0.7
        )
        fig.update_layout(
            height=340,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#8b949e'),
            xaxis=dict(showgrid=True, gridcolor='#21262d', title="Weight (kg)"),
            yaxis=dict(showgrid=True, gridcolor='#21262d', title="Height (cm)")
        )
        return fig

    @staticmethod
    def create_gender_comparison_chart(data: pd.DataFrame) -> go.Figure:
        fig = px.line(data, x="Year", y=["Male", "Female"], color_discrete_sequence=['#58a6ff', '#3fb950'])
        fig.update_layout(
            height=340,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#8b949e'),
            xaxis=dict(showgrid=True, gridcolor='#21262d'),
            yaxis=dict(showgrid=True, gridcolor='#21262d', title="Athletes Count"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        return fig
