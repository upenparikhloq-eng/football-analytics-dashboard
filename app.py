import streamlit as st
import pandas as pd
import sys

# Import analytics modules
sys.path.append("src")

from player_analytics import *
from team_analytics import *

# ----------------------------------
# PAGE CONFIG
# ----------------------------------

st.set_page_config(
    page_title="Football Analytics Dashboard",
    layout="wide"
)

st.title("⚽ Football Analytics Dashboard")
st.markdown("StatsBomb Open Data Analysis")

# ----------------------------------
# LOAD DATA
# ----------------------------------

@st.cache_data
def load_data():

    # CHANGE THIS PATH
    events = pd.read_json(
        "C:/Data_Analysis/Projects/football_analytics_dashboard/data/events/3869685.json"
    )

    return events

events = load_data()

# ----------------------------------
# SIDEBAR
# ----------------------------------

st.sidebar.header("Filters")

teams = sorted(
    events['team']
    .dropna()
    .apply(lambda x: x['name'])
    .unique()
)

team = st.sidebar.selectbox(
    "Select Team",
    teams
)

players = sorted(

    events[
        events['team'].apply(
            lambda x:
            x['name']
            if pd.notnull(x)
            else None
        ) == team
    ]['player']

    .dropna()

    .apply(
        lambda x: x['name']
    )

    .unique()
)

player = st.sidebar.selectbox(
    "Select Player",
    players
)

# ----------------------------------
# TABS
# ----------------------------------

player_tab, team_tab = st.tabs(
    [
        "Player Analytics",
        "Team Analytics"
    ]
)

# ==================================
# PLAYER TAB
# ==================================

with player_tab:

    st.header(f"👤 {player}")

    # Player Stats

    stats = get_player_stats(
        events,
        player
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Passes",
        stats["Passes"]
    )

    col2.metric(
        "Shots",
        stats["Shots"]
    )

    col3.metric(
        "Carries",
        stats["Carries"]
    )

    # Heatmap

    st.subheader("Player Heatmap")

    heatmap_fig = plot_player_heatmap(
        events,
        player
    )

    st.pyplot(
        heatmap_fig
    )

    # Pass Map

    st.subheader("Player Pass Map")

    passmap_fig = plot_player_passmap(
        events,
        player
    )

    st.pyplot(
        passmap_fig
    )

    # Shot Map

    st.subheader("Player Shot Map")

    shotmap_fig = plot_player_shotmap(
        events,
        player
    )

    st.pyplot(
        shotmap_fig
    )

    # Radar

    st.subheader("Player Radar")

    radar_fig = plot_player_radar(
        events,
        player
    )

    st.pyplot(
        radar_fig
    )

# ==================================
# TEAM TAB
# ==================================

with team_tab:

    st.header(f"🏆 {team}")

    team_stats = get_team_stats(
        events,
        team
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Passes",
        team_stats["Passes"]
    )

    col2.metric(
        "Shots",
        team_stats["Shots"]
    )

    col3.metric(
        "Carries",
        team_stats["Carries"]
    )

    # Average Positions

    st.subheader(
        "Average Positions"
    )

    avg_pos_fig = plot_average_positions(
        events,
        team
    )

    st.pyplot(
        avg_pos_fig
    )

    # Passing Network

    st.subheader(
        "Passing Network"
    )

    network_fig = plot_passing_network(
        events,
        team
    )

    st.pyplot(
        network_fig
    )

    # xG Timeline

    st.subheader(
        "xG Timeline"
    )

    xg_fig = plot_xg_timeline(
        events
    )

    st.pyplot(
        xg_fig
    )

    # Team Comparison

    st.subheader(
        "Argentina vs France Comparison"
    )

    comparison_fig = plot_team_comparison(
        events,
        "Argentina",
        "France"
    )

    st.pyplot(
        comparison_fig
    )