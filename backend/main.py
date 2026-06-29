from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

from src.player_analytics import get_player_stats
from src.team_analytics import get_team_stats
from src.player_analytics import get_normalized_radar_stats
from src.team_analytics import plot_average_positions
from src.team_analytics import plot_passing_network
from src.team_analytics import plot_xg_timeline
from src.team_analytics import plot_team_comparison
from src.player_analytics import plot_player_heatmap
from src.player_analytics import plot_player_passmap

from io import BytesIO
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import os



def save_plot(fig):

    buffer = BytesIO()

    fig.savefig(
        buffer,
        format="png",
        bbox_inches="tight"
    )

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="image/png"
    )


# =========================
# CREATE APP
# =========================

app = FastAPI()

# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://football-analytics-dashboard.vercel.app",
        "https://football-analytics-dashboard-jedh3mnv0-upen-parikh-s-projects.vercel.app",
        "https://football-analytics-dashboard-smoky.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# =========================
# LOAD DATA
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

events = pd.read_json(
    os.path.join(BASE_DIR, "data/events/3869685.json")
)

# =========================
# HOME
# =========================

@app.get("/")
def home():

    return {
        "message": "Football Analytics API Running"
    }

# =========================
# PLAYER STATS
# =========================

@app.get("/player-stats")
def player_stats(player_name: str):

    return get_player_stats(
        events,
        player_name
    )

@app.get("/player-pass-map")
def player_pass_map(player_name: str):

    fig = plot_player_passmap(
        events,
        player_name
    )

    return save_plot(fig)

@app.get("/player-heatmap")
def player_heatmap(player_name: str):

    fig =plot_player_heatmap (
        events,
        player_name
    )

    return save_plot(fig)

# =========================
# TEAM STATS
# =========================

@app.get("/team-stats")
def team_stats(team_name: str):

    return get_team_stats(
        events,
        team_name
    )

@app.get("/average-positions")
def average_positions(team_name: str):

    fig = plot_average_positions(
        events,
        team_name
    )

    return save_plot(fig)

@app.get("/passing-network")
def passing_network(team_name: str):

    fig = plot_passing_network(
        events,
        team_name
    )

    return save_plot(fig)

@app.get("/xg-timeline")
def xg_timeline():

    fig = plot_xg_timeline(events)

    return save_plot(fig)

@app.get("/team-comparison")
def team_comparison(
    team1: str,
    team2: str
):

    fig = plot_team_comparison(
        events,
        team1,
        team2
    )

    return save_plot(fig)

# =========================
# GET TEAMS
# =========================

@app.get("/teams")
def get_teams():

    teams = sorted(
        events["team"]
        .dropna()
        .apply(lambda x: x["name"])
        .unique()
        .tolist()
    )

    return teams

# =========================
# GET PLAYERS
# =========================

@app.get("/players")
def get_players(team_name: str):

    players = sorted(

        events[
            events["team"].apply(
                lambda x:
                x["name"]
                if pd.notnull(x)
                else None
            ) == team_name
        ]["player"]

        .dropna()

        .apply(
            lambda x: x["name"]
        )

        .unique()

        .tolist()
    )

    return players

@app.get("/player-radar")
def player_radar(player_name: str):

    return get_normalized_radar_stats(
        events,
        player_name
    )

@app.get("/compare-radar")
def compare_radar(
    player1: str,
    player2: str
):

    return {
        "player1": {
            "name": player1,
            "stats": get_normalized_radar_stats(
                events,
                player1
            )
        },
        "player2": {
            "name": player2,
            "stats": get_normalized_radar_stats(
                events,
                player2
            )
        }
    }