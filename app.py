import streamlit as st
import pandas as pd
import plotly.express as px
from olympics.pipeline import OlympicAnalyticsPipeline
from olympics.utils import ChartBuilder

st.set_page_config(
    page_title="Olympic Data Analytics: 120 Years",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"], .stApp {
        font-family: 'Inter', sans-serif;
        background-color: #0d1117 !important;
        color: #e6edf3 !important;
    }
    
    header, [data-testid="stToolbar"], [data-testid="stHeader"] {
        display: none !important;
    }
    
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1440px !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #30363d !important;
    }
    
    .nav-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px 24px;
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 22px;
        font-weight: 800;
        color: #f0f6fc;
        letter-spacing: -0.5px;
    }
    
    .nav-badge {
        background: rgba(56, 139, 253, 0.15);
        color: #58a6ff;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 600;
        border: 1px solid rgba(56, 139, 253, 0.3);
    }
    
    .kpi-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 24px;
    }
    
    .kpi-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 16px 20px;
    }
    
    .kpi-title {
        font-size: 12px;
        font-weight: 600;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    
    .kpi-value {
        font-size: 30px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.5px;
    }
    
    .card-panel {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    .card-title {
        font-size: 14px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        color: #8b949e;
        margin-bottom: 16px;
    }
    
    label, p, span {
        color: #c9d1d9 !important;
        font-size: 13px !important;
    }
    
    div[data-baseweb="select"] > div,
    input {
        background-color: #0d1117 !important;
        color: #f0f6fc !important;
        border: 1px solid #30363d !important;
        border-radius: 6px !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_pipeline():
    return OlympicAnalyticsPipeline(season='Summer')

pipeline = get_pipeline()
stats = pipeline.get_summary_statistics()

st.sidebar.markdown("<h2 style='color:#58a6ff; font-weight:800; font-size:20px; margin-bottom:15px;'>Navigation</h2>", unsafe_allow_html=True)
user_menu = st.sidebar.radio(
    'Select Analytics Module',
    ('Medal Tally', 'Historical Trends', 'Country Deep Dive', 'Athlete Demographics')
)

st.markdown("""
<div class="nav-bar">
    <div class="nav-brand">
        <span>OLYMPIC DATA ANALYTICS: 120 YEARS</span>
        <span class="nav-badge">1896 – 2016</span>
    </div>
    <div style="font-size: 13px; color: #8b949e;">
        Interactive Multi-dimensional Intelligence Platform
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="kpi-row">
    <div class="kpi-card" style="border-left: 4px solid #58a6ff;">
        <div class="kpi-title">Total Nations</div>
        <div class="kpi-value">{stats['nations']}</div>
    </div>
    <div class="kpi-card" style="border-left: 4px solid #3fb950;">
        <div class="kpi-title">Total Athletes</div>
        <div class="kpi-value">{stats['athletes']:,}</div>
    </div>
    <div class="kpi-card" style="border-left: 4px solid #d29922;">
        <div class="kpi-title">Olympic Editions</div>
        <div class="kpi-value">{stats['editions']}</div>
    </div>
    <div class="kpi-card" style="border-left: 4px solid #f0883e;">
        <div class="kpi-title">Medal Records</div>
        <div class="kpi-value">{stats['medals_awarded']:,}</div>
    </div>
</div>
""", unsafe_allow_html=True)

if user_menu == 'Medal Tally':
    st.sidebar.markdown("<hr style='border-color:#30363d;'/>", unsafe_allow_html=True)
    st.sidebar.markdown("<h4 style='color:#8b949e; font-size:13px; text-transform:uppercase;'>Filters</h4>", unsafe_allow_html=True)
    years, countries = pipeline.medal_analyzer.get_filter_options()
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", countries)
    
    medal_tally = pipeline.medal_analyzer.calculate_medal_tally(selected_year, selected_country)
    
    col1, col2 = st.columns([1.3, 1], gap="large")
    
    with col1:
        st.markdown('<div class="card-panel">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Global Medal Distribution Map</div>', unsafe_allow_html=True)
        map_df = pipeline.medal_analyzer.calculate_medal_tally(selected_year, 'Overall')
        fig_map = ChartBuilder.create_choropleth_map(map_df)
        st.plotly_chart(fig_map, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="card-panel">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Top 10 Countries by Medal Type</div>', unsafe_allow_html=True)
        
        if selected_country == 'Overall':
            fig_bar = ChartBuilder.create_stacked_medal_bar(medal_tally)
            st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
        else:
            fig_donut = px.pie(
                values=[medal_tally['Gold'].sum(), medal_tally['Silver'].sum(), medal_tally['Bronze'].sum()],
                names=['Gold', 'Silver', 'Bronze'],
                color=['Gold', 'Silver', 'Bronze'],
                color_discrete_map={'Gold': '#d29922', 'Silver': '#94a3b8', 'Bronze': '#b45309'},
                hole=0.5
            )
            fig_donut.update_layout(
                height=320,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#8b949e')
            )
            st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})
            
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card-panel">', unsafe_allow_html=True)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.markdown('<div class="card-title">Overall Historical Medal Tally Leaderboard</div>', unsafe_allow_html=True)
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.markdown(f'<div class="card-title">Medal Tally for {selected_year} Olympics</div>', unsafe_allow_html=True)
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.markdown(f'<div class="card-title">Historical Medal Tally for {selected_country}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="card-title">Medal Tally for {selected_country} in {selected_year}</div>', unsafe_allow_html=True)
        
    st.dataframe(medal_tally, use_container_width=True, height=280)
    st.markdown('</div>', unsafe_allow_html=True)

elif user_menu == 'Historical Trends':
    nations_over_time = pipeline.trend_analyzer.get_metrics_over_time('region')
    events_over_time = pipeline.trend_analyzer.get_metrics_over_time('Event')
    
    t_col1, t_col2 = st.columns(2, gap="large")
    
    with t_col1:
        st.markdown('<div class="card-panel">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Participating Nations Over Time</div>', unsafe_allow_html=True)
        fig1 = ChartBuilder.create_line_chart(nations_over_time, "Edition", "region", '#58a6ff')
        st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
        
    with t_col2:
        st.markdown('<div class="card-panel">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Events Growth Over Time</div>', unsafe_allow_html=True)
        fig2 = ChartBuilder.create_line_chart(events_over_time, "Edition", "Event", '#3fb950')
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card-panel">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Number of Events Over Time (Every Sport)</div>', unsafe_allow_html=True)
    sport_matrix = pipeline.trend_analyzer.get_sport_event_matrix()
    fig_heat = ChartBuilder.create_heatmap(sport_matrix, color_scale="Viridis", height=540)
    st.plotly_chart(fig_heat, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card-panel">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Most Successful Athletes Leaderboard</div>', unsafe_allow_html=True)
    sport_list = pipeline.df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Filter by Sport', sport_list)
    successful_df = pipeline.trend_analyzer.get_most_successful_athletes(selected_sport)
    st.dataframe(successful_df, use_container_width=True, height=260)
    st.markdown('</div>', unsafe_allow_html=True)

elif user_menu == 'Country Deep Dive':
    country_list = pipeline.country_analyzer.get_country_list()
    default_index = country_list.index('USA') if 'USA' in country_list else 0
    selected_c = st.sidebar.selectbox('Select Country', country_list, index=default_index)

    country_df = pipeline.country_analyzer.get_country_medal_trajectory(selected_c)
    
    st.markdown('<div class="card-panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="card-title">{selected_c} Medal Trajectory Over Time</div>', unsafe_allow_html=True)
    if not country_df.empty:
        fig_c = ChartBuilder.create_line_chart(country_df, "Year", "Medal", '#f0883e')
        st.plotly_chart(fig_c, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info(f"No medal records found for {selected_c}.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card-panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="card-title">Sports Dominance Matrix for {selected_c}</div>', unsafe_allow_html=True)
    pt = pipeline.country_analyzer.get_country_sport_heatmap(selected_c)
    if not pt.empty:
        fig_pt = ChartBuilder.create_heatmap(pt, color_scale="Magma", height=340)
        st.plotly_chart(fig_pt, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info(f"No sports matrix data available for {selected_c}.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card-panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="card-title">Top 10 Athletes of {selected_c}</div>', unsafe_allow_html=True)
    top10_df = pipeline.country_analyzer.get_top_country_athletes(selected_c)
    st.dataframe(top10_df, use_container_width=True, height=260)
    st.markdown('</div>', unsafe_allow_html=True)

elif user_menu == 'Athlete Demographics':
    st.markdown('<div class="card-panel">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Age Distribution of Medalists</div>', unsafe_allow_html=True)
    overall_age, gold_age, silver_age, bronze_age = pipeline.demographic_analyzer.get_age_distributions()
    fig_age = ChartBuilder.create_age_distribution_plot(overall_age, gold_age, silver_age, bronze_age)
    st.plotly_chart(fig_age, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

    d_col1, d_col2 = st.columns(2, gap="large")
    
    with d_col1:
        st.markdown('<div class="card-panel">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Height vs Weight Analysis</div>', unsafe_allow_html=True)
        sport_list = pipeline.df['Sport'].unique().tolist()
        sport_list.sort()
        sport_list.insert(0, 'Overall')
        selected_s = st.selectbox('Select Sport for Scatter', sport_list)
        temp_hw = pipeline.demographic_analyzer.get_physical_data_by_sport(selected_s)
        fig_hw = ChartBuilder.create_scatter_plot(temp_hw)
        st.plotly_chart(fig_hw, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    with d_col2:
        st.markdown('<div class="card-panel">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Historical Athlete Participation (Men vs Women)</div>', unsafe_allow_html=True)
        final_gender = pipeline.demographic_analyzer.get_gender_participation_history()
        fig_gender = ChartBuilder.create_gender_comparison_chart(final_gender)
        st.plotly_chart(fig_gender, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)