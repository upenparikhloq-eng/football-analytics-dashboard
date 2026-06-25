import pandas as pd
import matplotlib.pyplot as plt

from mplsoccer import Pitch
from matplotlib.colors import LinearSegmentedColormap

def format_player_name(name):

    custom_names = {
        'Lionel Andrés Messi Cuccittini': 'Messi',
        'Kylian Mbappé Lottin': 'Mbappe',
        'Rodrigo Javier De Paul': 'De Paul',
        'Alexis Mac Allister': 'Mac Allister',
        'Ángel Fabián Di María Hernández': 'Di Maria',
        'Julián Álvarez': 'Alvarez',
        'Aurélien Djani Tchouaméni': 'Tchouameni',
        'Antoine Griezmann': 'Griezmann',
        'Adrien Rabiot': 'Rabiot',
        'Raphaël Varane': 'Varane'
    }

    return custom_names.get(
        name,
        name.split()[-1]
    )
# =========================
# PLAYER STATS
# =========================

def get_player_stats(events, player_name):

    player_events = events[
        events['player'].apply(
            lambda x: x['name'] if pd.notnull(x) else None
        ) == player_name
    ]

    event_counts = player_events['type'].apply(
        lambda x: x['name'] if pd.notnull(x) else None
    ).value_counts()

    stats = {
        'Player': player_name,
        'Total Events': int(len(player_events)),
        'Passes': int(event_counts.get('Pass', 0)),
        'Shots': int(event_counts.get('Shot', 0)),
        'Carries': int(event_counts.get('Carry', 0)),
        'Dribbles': int(event_counts.get('Dribble', 0)),
        'Pressures': int(event_counts.get('Pressure', 0)),
        'Ball Recoveries': int(event_counts.get('Ball Recovery', 0))
    }

    return stats


# =========================
# PLAYER LOCATIONS
# =========================

def get_player_locations(events, player_name):

    player_events = events[
        events['player'].apply(
            lambda x: x['name'] if pd.notnull(x) else None
        ) == player_name
    ]

    locations = player_events['location'].dropna()

    x = locations.apply(lambda loc: loc[0])
    y = locations.apply(lambda loc: loc[1])

    return x, y


# =========================
# PLAYER HEATMAP
# =========================

def plot_player_heatmap(events, player_name):

    x, y = get_player_locations(events, player_name)

    heatmap_colors = LinearSegmentedColormap.from_list(
        "custom_heatmap",
        [
            '#fefae0',
            '#ffb703',
            '#fb8500',
            '#d00000'
        ]
    )

    pitch = Pitch(
        pitch_type='statsbomb',
        pitch_color='#1B4332',
        line_color='white',
        linewidth=2
    )

    fig, ax = pitch.draw(figsize=(12, 8))

    pitch.kdeplot(
        x=x,
        y=y,
        fill=True,
        levels=100,
        thresh=0.05,
        bw_adjust=0.7,
        cmap=heatmap_colors,
        alpha=0.9,
        ax=ax
    )

    pitch.scatter(
        x,
        y,
        s=15,
        color='white',
        alpha=0.15,
        ax=ax
    )

    fig.set_facecolor('#1B4332')
    ax.set_facecolor('#1B4332')

    ax.set_title(
        f"{player_name} Heatmap",
        color='white',
        fontsize=18,
        pad=20,
        fontweight='bold'
    )

    return fig


# =========================
# PLAYER SHOTS
# =========================

def get_player_shots(events, player_name):

    shots = events[
        events['type'].apply(
            lambda x: x['name'] if pd.notnull(x) else None
        ) == 'Shot'
    ]

    player_shots = shots[
        shots['player'].apply(
            lambda x: x['name'] if pd.notnull(x) else None
        ) == player_name
    ]

    shot_data = []

    for _, shot in player_shots.iterrows():

        shot_info = shot['shot']

        shot_data.append({
            'x': shot['location'][0],
            'y': shot['location'][1],
            'xG': shot_info.get('statsbomb_xg', 0),
            'Outcome': shot_info['outcome']['name']
        })

    return pd.DataFrame(shot_data)


# =========================
# SHOT MAP
# =========================

def plot_player_shotmap(events, player_name):

    shots_df = get_player_shots(events, player_name)

    pitch = Pitch(
        pitch_type='statsbomb',
        pitch_color='#1B4332',
        line_color='white',
        linewidth=2,
        half=True
    )

    fig, ax = pitch.draw(figsize=(12, 8))

    goals = shots_df[
        shots_df['Outcome'] == 'Goal'
    ]

    non_goals = shots_df[
        shots_df['Outcome'] != 'Goal'
    ]

    pitch.scatter(
        non_goals['x'],
        non_goals['y'],
        s=non_goals['xG'] * 3000,
        color='white',
        edgecolors='black',
        alpha=0.7,
        ax=ax
    )

    pitch.scatter(
        goals['x'],
        goals['y'],
        s=goals['xG'] * 3000,
        color='lime',
        edgecolors='black',
        alpha=0.9,
        ax=ax
    )

    fig.set_facecolor('#1B4332')

    ax.set_title(
        f"{player_name} Shot Map",
        color='white',
        fontsize=18
    )

    return fig


# =========================
# PLAYER PASSES
# =========================

def get_player_passes(events, player_name):

    passes = events[
        events['type'].apply(
            lambda x: x['name'] if pd.notnull(x) else None
        ) == 'Pass'
    ]

    player_passes = passes[
        passes['player'].apply(
            lambda x: x['name'] if pd.notnull(x) else None
        ) == player_name
    ]

    pass_data = []

    for _, row in player_passes.iterrows():

        pass_info = row['pass']

        pass_data.append({
            'x': row['location'][0],
            'y': row['location'][1],
            'end_x': pass_info['end_location'][0],
            'end_y': pass_info['end_location'][1],
            'successful': 'outcome' not in pass_info
        })

    return pd.DataFrame(pass_data)


def get_pass_accuracy(pass_df):

    total_passes = len(pass_df)

    successful_passes = pass_df['successful'].sum()

    accuracy = round(
        successful_passes / total_passes * 100,
        2
    )

    return accuracy


# =========================
# PASS MAP
# =========================

def plot_player_passmap(events, player_name):

    pass_df = get_player_passes(
        events,
        player_name
    )

    accuracy = get_pass_accuracy(pass_df)

    pitch = Pitch(
        pitch_type='statsbomb',
        pitch_color='#1B4332',
        line_color='white',
        linewidth=2
    )

    fig, ax = pitch.draw(figsize=(12, 8))

    successful = pass_df[
        pass_df['successful']
    ]

    unsuccessful = pass_df[
        ~pass_df['successful']
    ]

    pitch.arrows(
        successful['x'],
        successful['y'],
        successful['end_x'],
        successful['end_y'],
        color='#00ff88',
        width=1.5,
        ax=ax
    )

    pitch.arrows(
        unsuccessful['x'],
        unsuccessful['y'],
        unsuccessful['end_x'],
        unsuccessful['end_y'],
        color='#ff4d4d',
        width=1.5,
        ax=ax
    )

    fig.set_facecolor('#1B4332')

    ax.set_title(
        f"{player_name}\nPass Accuracy: {accuracy}%",
        color='white',
        fontsize=18
    )

    return fig

import pandas as pd


def get_player_radar_stats(events, player_name):

    player_events = events[
        events['player'].apply(
            lambda x: x['name']
            if pd.notnull(x) else None
        ) == player_name
    ]

    event_counts = player_events['type'].apply(
        lambda x: x['name']
        if pd.notnull(x) else None
    ).value_counts()

    stats = {

        'Passes':
            int(event_counts.get('Pass', 0)),

        'Shots':
            int(event_counts.get('Shot', 0)),

        'Carries':
            int(event_counts.get('Carry', 0)),

        'Dribbles':
            int(event_counts.get('Dribble', 0)),

        'Pressures':
            int(event_counts.get('Pressure', 0)),

        'Recoveries':
            int(event_counts.get('Ball Recovery', 0))
    }

    return stats

import matplotlib.pyplot as plt
import numpy as np

def plot_player_radar(events, player_name):

    stats = get_player_radar_stats(
        events,
        player_name
    )

    labels = list(stats.keys())
    values = list(stats.values())

    values += values[:1]
    labels += labels[:1]

    angles = np.linspace(
        0,
        2 * np.pi,
        len(labels),
        endpoint=True
    )

    fig, ax = plt.subplots(
        figsize=(8, 8),
        subplot_kw=dict(polar=True)
    )

    ax.plot(
        angles,
        values,
        linewidth=3,
        color='#ffb703'
    )

    ax.fill(
        angles,
        values,
        color='#ffb703',
        alpha=0.4
    )

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(
        labels[:-1],
        fontsize=11
    )

    ax.set_title(
        player_name,
        fontsize=16,
        fontweight='bold',
        pad=20
    )

    return fig

def get_normalized_radar_stats(events, player_name):

    metrics = [
        'Pass',
        'Shot',
        'Carry',
        'Dribble',
        'Pressure',
        'Ball Recovery'
    ]

    players = events['player'].dropna().apply(
        lambda x: x['name']
    ).unique()

    radar_data = []

    for player in players:

        player_events = events[
            events['player'].apply(
                lambda x: x['name']
                if pd.notnull(x) else None
            ) == player
        ]

        event_counts = player_events['type'].apply(
            lambda x: x['name']
            if pd.notnull(x) else None
        ).value_counts()

        radar_data.append({

            'player': player,

            'Passes':
                event_counts.get('Pass', 0),

            'Shots':
                event_counts.get('Shot', 0),

            'Carries':
                event_counts.get('Carry', 0),

            'Dribbles':
                event_counts.get('Dribble', 0),

            'Pressures':
                event_counts.get('Pressure', 0),

            'Recoveries':
                event_counts.get('Ball Recovery', 0)
        })

    radar_df = pd.DataFrame(radar_data)

    player_row = radar_df[
        radar_df['player'] == player_name
    ]

    normalized = {}

    for col in radar_df.columns[1:]:

        max_value = radar_df[col].max()

        normalized[col] = round(
            (
                player_row[col].iloc[0]
                / max_value
            ) * 100,
            1
        )

    return normalized

import numpy as np
import matplotlib.pyplot as plt

def compare_player_radars(events, *players):

    colors = [
        '#6CB4EE',
        '#d00000',
        '#ffb703',
        '#00b4d8',
        '#8338ec'
    ]

    fig, ax = plt.subplots(
        figsize=(9, 9),
        subplot_kw=dict(polar=True)
    )

    for i, player in enumerate(players):

        stats = get_normalized_radar_stats(
            events,
            player
        )

        categories = list(stats.keys())

        values = list(stats.values())
        values += values[:1]

        angles = np.linspace(
            0,
            2 * np.pi,
            len(categories),
            endpoint=False
        ).tolist()

        angles += angles[:1]

        ax.plot(
            angles,
            values,
            linewidth=3,
            color=colors[i % len(colors)],
            label=format_player_name(player)
        )

        ax.fill(
            angles,
            values,
            color=colors[i % len(colors)],
            alpha=0.15
        )

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(
        categories,
        fontsize=11,
        fontweight='bold'
    )

    ax.set_ylim(0, 100)

    ax.set_title(
        "Player Radar Comparison",
        fontsize=18,
        fontweight='bold'
    )

    ax.legend(
        bbox_to_anchor=(1.25, 1.1)
    )

    return fig