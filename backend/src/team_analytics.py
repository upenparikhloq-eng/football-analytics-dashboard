import pandas as pd
import matplotlib.pyplot as plt

from mplsoccer import Pitch


# ==================================
# TEAM STATS
# ==================================

def get_team_stats(events, team_name):

    team_events = events[
        events['team'].apply(
            lambda x: x['name'] if pd.notnull(x) else None
        ) == team_name
    ]

    event_counts = team_events['type'].apply(
        lambda x: x['name'] if pd.notnull(x) else None
    ).value_counts()

    stats = {
        'Team': team_name,
        'Total Events': int(len(team_events)),
        'Passes': int(event_counts.get('Pass', 0)),
        'Shots': int(event_counts.get('Shot', 0)),
        'Carries': int(event_counts.get('Carry', 0)),
        'Pressures': int(event_counts.get('Pressure', 0)),
        'Ball Recoveries': int(event_counts.get('Ball Recovery', 0))
    }

    return stats


# ==================================
# AVERAGE POSITIONS
# ==================================

def get_average_positions(events, team_name):

    team_events = events[
        events['team'].apply(
            lambda x: x['name'] if pd.notnull(x) else None
        ) == team_name
    ]

    team_events = team_events[
        team_events['player'].notna() &
        team_events['location'].notna()
    ]

    player_positions = []

    for player in team_events['player'].apply(
        lambda x: x['name']
    ).unique():

        player_events = team_events[
            team_events['player'].apply(
                lambda x: x['name']
            ) == player
        ]

        avg_x = player_events['location'].apply(
            lambda loc: loc[0]
        ).mean()

        avg_y = player_events['location'].apply(
            lambda loc: loc[1]
        ).mean()

        touches = len(player_events)

        player_positions.append({
            'player': player,
            'avg_x': avg_x,
            'avg_y': avg_y,
            'touches': touches
        })

    return pd.DataFrame(player_positions)


# ==================================
# PLAYER NAME FORMATTER
# ==================================

def format_player_name(name):

    custom_names = {

        # Argentina
        'Lionel Andrés Messi Cuccittini': 'Messi',
        'Rodrigo Javier De Paul': 'De Paul',
        'Alexis Mac Allister': 'Mac Allister',
        'Ángel Fabián Di María Hernández': 'Di Maria',
        'Damián Emiliano Martínez': 'Emi',
        'Julián Álvarez': 'Alvarez',
        'Cristian Gabriel Romero': 'Romero',
        'Nicolás Hernán Otamendi': 'Otamendi',
        'Enzo Fernandez': 'Enzo',
        'Nahuel Molina Lucero': 'Molina',
        'Nicolás Alejandro Tagliafico': 'Tagliafico',

        # France
        'Kylian Mbappé Lottin': 'Mbappe',
        'Antoine Griezmann': 'Griezmann',
        'Adrien Rabiot': 'Rabiot',
        'Aurélien Djani Tchouaméni': 'Tchouameni',
        'Theo Bernard François Hernández': 'Theo',
        'Jules Koundé': 'Kounde',
        'Raphaël Varane': 'Varane',
        'Dayotchanculle Upamecano': 'Upamecano',
        'Hugo Lloris': 'Lloris',
        'Olivier Giroud': 'Giroud'
    }

    return custom_names.get(
        name,
        name.split()[-1]
    )


# ==================================
# AVERAGE POSITION MAP
# ==================================

def plot_average_positions(events, team_name):

    avg_positions = get_average_positions(
        events,
        team_name
    )

    # Remove low-touch substitutes
    avg_positions = avg_positions[
        avg_positions['touches'] >= 50
    ]

    pitch = Pitch(
        pitch_type='statsbomb',
        pitch_color='#1B4332',
        line_color='white',
        linewidth=2
    )

    fig, ax = pitch.draw(
        figsize=(14, 9)
    )

    # Player circles
    pitch.scatter(
        avg_positions['avg_x'],
        avg_positions['avg_y'],
        s=avg_positions['touches'] * 5,
        color='#ffb703',
        edgecolors='black',
        linewidth=2,
        alpha=0.95,
        ax=ax
    )

    # Player labels
    for _, row in avg_positions.iterrows():

        player_label = format_player_name(
            row['player']
        )

        ax.text(
            row['avg_x'],
            row['avg_y'],
            player_label,
            color='white',
            fontsize=8,
            fontweight='bold',
            ha='center',
            va='center'
        )

    fig.set_facecolor('#1B4332')
    ax.set_facecolor('#1B4332')

    ax.set_title(
        f"{team_name} Average Positions",
        fontsize=20,
        color='white',
        fontweight='bold',
        pad=20
    )

    return fig

def get_pass_network_data(events, team_name):

    # Team passes only
    passes = events[
        (events['team'].apply(
            lambda x: x['name'] if pd.notnull(x) else None
        ) == team_name)
        &
        (events['type'].apply(
            lambda x: x['name'] if pd.notnull(x) else None
        ) == 'Pass')
    ]

    pass_pairs = []

    for _, row in passes.iterrows():

        passer = row['player']['name']

        recipient = row['pass'].get('recipient')

        if recipient is None:
            continue

        recipient = recipient['name']

        pass_pairs.append({
            'passer': passer,
            'recipient': recipient
        })

    pass_network = (
        pd.DataFrame(pass_pairs)
        .groupby(['passer', 'recipient'])
        .size()
        .reset_index(name='pass_count')
    )

    return pass_network

def plot_passing_network(events, team_name):

    avg_positions = get_average_positions(
        events,
        team_name
    )

    avg_positions = avg_positions[
        avg_positions['touches'] >= 50
    ]

    network = get_pass_network_data(
        events,
        team_name
    )

    # Keep only strong connections
    network = network.nlargest(
        25,
        'pass_count')

    pitch = Pitch(
        pitch_type='statsbomb',
        pitch_color='#1B4332',
        line_color='white',
        linewidth=2
    )

    fig, ax = pitch.draw(
        figsize=(14, 9)
    )

    # ------------------------
    # Draw Pass Lines
    # ------------------------

    for _, row in network.iterrows():

        passer = row['passer']
        recipient = row['recipient']

        passer_row = avg_positions[
            avg_positions['player'] == passer
        ]

        recipient_row = avg_positions[
            avg_positions['player'] == recipient
        ]

        if passer_row.empty or recipient_row.empty:
            continue

        x1 = passer_row['avg_x'].values[0]
        y1 = passer_row['avg_y'].values[0]

        x2 = recipient_row['avg_x'].values[0]
        y2 = recipient_row['avg_y'].values[0]

        pitch.lines(
            x1,
            y1,
            x2,
            y2,
            lw=row['pass_count'] / network['pass_count'].max() * 8,
            color='#ffb703',
            alpha=0.5,
            ax=ax
        )

    # ------------------------
    # Draw Nodes
    # ------------------------

    pitch.scatter(
        avg_positions['avg_x'],
        avg_positions['avg_y'],
        s=avg_positions['touches'] * 5,
        color='#d00000',
        edgecolors='white',
        linewidth=2,
        ax=ax
    )

    # ------------------------
    # Labels
    # ------------------------

    for _, row in avg_positions.iterrows():

        ax.text(
            row['avg_x'],
            row['avg_y'],
            format_player_name(row['player']),
            color='white',
            fontsize=8,
            fontweight='bold',
            ha='center',
            va='center'
        )

    ax.set_title(
        f"{team_name} Passing Network",
        fontsize=20,
        color='white',
        fontweight='bold',
        pad=20
    )

    fig.set_facecolor('#1B4332')

    return fig

def get_team_xg(events, team_name):

    shots = events[
        events['type'].apply(
            lambda x: x['name'] if pd.notnull(x) else None
        ) == 'Shot'
    ]

    team_shots = shots[
        shots['team'].apply(
            lambda x: x['name'] if pd.notnull(x) else None
        ) == team_name
    ]

    total_xg = 0

    for _, shot in team_shots.iterrows():

        shot_data = shot['shot']

        total_xg += shot_data.get(
            'statsbomb_xg',
            0
        )

    return round(total_xg, 2)

def get_player_xg(events, team_name):

    shots = events[
        events['type'].apply(
            lambda x: x['name'] if pd.notnull(x) else None
        ) == 'Shot'
    ]

    team_shots = shots[
        shots['team'].apply(
            lambda x: x['name'] if pd.notnull(x) else None
        ) == team_name
    ]

    player_xg = []

    for player in team_shots['player'].apply(
        lambda x: x['name']
    ).unique():

        player_shots = team_shots[
            team_shots['player'].apply(
                lambda x: x['name']
            ) == player
        ]

        xg = player_shots['shot'].apply(
            lambda x: x.get('statsbomb_xg', 0)
        ).sum()

        player_xg.append({
            'player': player,
            'xG': round(xg, 2)
        })

    return pd.DataFrame(
        player_xg
    ).sort_values(
        by='xG',
        ascending=False
    )

def get_xg_timeline(events):

    shots = events[
        events['type'].apply(
            lambda x: x['name'] if pd.notnull(x) else None
        ) == 'Shot'
    ].copy()

    shots = shots.sort_values(
        by=['minute', 'second']
    )

    argentina_xg = 0
    france_xg = 0

    timeline = []

    for _, shot in shots.iterrows():

        team = shot['team']['name']

        shot_xg = shot['shot'].get(
            'statsbomb_xg',
            0
        )

        if team == 'Argentina':
            argentina_xg += shot_xg

        elif team == 'France':
            france_xg += shot_xg

        timeline.append({
            'minute': shot['minute'],
            'Argentina': argentina_xg,
            'France': france_xg
        })

    return pd.DataFrame(timeline)

import matplotlib.pyplot as plt
import pandas as pd


def plot_xg_timeline(events):

    timeline = get_xg_timeline(events)

    # Team colors
    argentina_color = '#6CB4EE'
    france_color = '#1D3557'

    fig, ax = plt.subplots(
        figsize=(14, 7)
    )

    # Background
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    # xG progression lines
    ax.step(
        timeline['minute'],
        timeline['Argentina'],
        where='post',
        color=argentina_color,
        linewidth=3,
        label='Argentina'
    )

    ax.step(
        timeline['minute'],
        timeline['France'],
        where='post',
        color=france_color,
        linewidth=3,
        label='France'
    )

    # Half-time
    ax.axvline(
        x=45,
        linestyle='--',
        color='gray',
        alpha=0.5
    )

    # Full-time
    ax.axvline(
        x=90,
        linestyle='--',
        color='gray',
        alpha=0.5
    )

    # Extra-time end
    ax.axvline(
        x=120,
        linestyle='--',
        color='gray',
        alpha=0.5
    )

    # Final xG labels
    ax.text(
        timeline['minute'].iloc[-1] + 1,
        timeline['Argentina'].iloc[-1],
        f"{timeline['Argentina'].iloc[-1]:.2f}",
        color=argentina_color,
        fontsize=12,
        fontweight='bold'
    )

    ax.text(
        timeline['minute'].iloc[-1] + 1,
        timeline['France'].iloc[-1],
        f"{timeline['France'].iloc[-1]:.2f}",
        color=france_color,
        fontsize=12,
        fontweight='bold'
    )

    # Goal markers
    shots = events[
        events['type'].apply(
            lambda x: x['name']
            if pd.notnull(x) else None
        ) == 'Shot'
    ]

    goals = shots[
        shots['shot'].apply(
            lambda x:
            x.get('outcome', {}).get('name')
            == 'Goal'
        )
    ]

    argentina_xg = 0
    france_xg = 0

    for _, shot in shots.sort_values(
        ['minute', 'second']
    ).iterrows():

        team = shot['team']['name']
        shot_xg = shot['shot'].get(
            'statsbomb_xg',
            0
        )

        if team == 'Argentina':
            argentina_xg += shot_xg
            current_xg = argentina_xg
            color = argentina_color
        else:
            france_xg += shot_xg
            current_xg = france_xg
            color = france_color

        outcome = shot['shot'].get(
            'outcome', {}
        ).get('name')

        if outcome == 'Goal':

            ax.scatter(
                shot['minute'],
                current_xg,
                s=180,
                color=color,
                edgecolors='black',
                zorder=5
            )

            ax.text(
                shot['minute'],
                current_xg + 0.15,
                '⚽',
                fontsize=12,
                ha='center'
            )

    # Styling
    ax.set_title(
        'Argentina vs France (2022 World Cup Final)\nExpected Goals Timeline',
        fontsize=18,
        fontweight='bold',
        pad=15
    )

    ax.set_xlabel(
        'Minute',
        fontsize=12
    )

    ax.set_ylabel(
        'Cumulative xG',
        fontsize=12
    )

    ax.grid(
        alpha=0.25,
        linestyle='--'
    )

    ax.legend(
        frameon=False,
        fontsize=11
    )

    plt.tight_layout()

    return fig

def compare_teams(events, team1, team2):

    team1_stats = get_team_stats(
        events,
        team1
    )

    team2_stats = get_team_stats(
        events,
        team2
    )

    comparison = pd.DataFrame({

        'Metric': [
            'Passes',
            'Shots',
            'Carries',
            'Pressures',
            'Ball Recoveries'
        ],

        team1: [
            team1_stats['Passes'],
            team1_stats['Shots'],
            team1_stats['Carries'],
            team1_stats['Pressures'],
            team1_stats['Ball Recoveries']
        ],

        team2: [
            team2_stats['Passes'],
            team2_stats['Shots'],
            team2_stats['Carries'],
            team2_stats['Pressures'],
            team2_stats['Ball Recoveries']
        ]

    })

    return comparison

def compare_teams_with_xg(events, team1, team2):

    comparison = compare_teams(
        events,
        team1,
        team2
    )

    xg_row = pd.DataFrame({

        'Metric': ['xG'],

        team1: [
            get_team_xg(
                events,
                team1
            )
        ],

        team2: [
            get_team_xg(
                events,
                team2
            )
        ]

    })

    comparison = pd.concat(
        [comparison, xg_row],
        ignore_index=True
    )

    return comparison

import matplotlib.pyplot as plt
import numpy as np


def plot_team_comparison(events, team1, team2):

    comparison = compare_teams_with_xg(
        events,
        team1,
        team2
    )

    metrics = comparison['Metric']

    team1_values = comparison[team1]
    team2_values = comparison[team2]

    y = np.arange(len(metrics))

    fig, ax = plt.subplots(
        figsize=(12, 7)
    )

    # Team bars
    ax.barh(
        y + 0.2,
        team1_values,
        height=0.35,
        color='#6CB4EE',
        label=team1
    )

    ax.barh(
        y - 0.2,
        team2_values,
        height=0.35,
        color='#1D3557',
        label=team2
    )

    # Value labels
    for i, value in enumerate(team1_values):

        ax.text(
            value + max(team1_values.max(), team2_values.max()) * 0.01,
            i + 0.2,
            str(round(value, 2)),
            va='center',
            fontsize=10,
            fontweight='bold'
        )

    for i, value in enumerate(team2_values):

        ax.text(
            value + max(team1_values.max(), team2_values.max()) * 0.01,
            i - 0.2,
            str(round(value, 2)),
            va='center',
            fontsize=10,
            fontweight='bold'
        )

    # Formatting
    ax.set_yticks(y)
    ax.set_yticklabels(
        metrics,
        fontsize=11,
        fontweight='bold'
    )

    ax.set_xlabel(
        'Value',
        fontsize=12,
        fontweight='bold'
    )

    ax.set_title(
        f'{team1} vs {team2}\nMatch Statistics Comparison',
        fontsize=18,
        fontweight='bold',
        pad=20
    )

    ax.grid(
        axis='x',
        linestyle='--',
        alpha=0.3
    )

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.legend(
        fontsize=11,
        frameon=False
    )

    plt.tight_layout()

    return fig

def get_pass_network(events, team_name):

    # Team passes only
    passes = events[
        (events['type'].apply(
            lambda x: x['name'] if pd.notnull(x) else None
        ) == 'Pass')
    ]

    passes = passes[
        passes['team'].apply(
            lambda x: x['name'] if pd.notnull(x) else None
        ) == team_name
    ]

    network_data = []

    for _, row in passes.iterrows():

        passer = row['player']['name']

        if pd.notnull(row['pass'].get('recipient')):

            recipient = row['pass']['recipient']['name']

            network_data.append({
                'passer': passer,
                'recipient': recipient
            })

    network_df = pd.DataFrame(network_data)

    pass_counts = (
        network_df
        .groupby(['passer', 'recipient'])
        .size()
        .reset_index(name='pass_count')
    )

    return pass_counts

from mplsoccer import Pitch
import matplotlib.pyplot as plt


def plot_passing_network(events, team_name):

    avg_positions = get_average_positions(
        events,
        team_name
    )

    avg_positions = avg_positions[
        avg_positions['touches'] >= 50
    ]

    pass_network = get_pass_network(
        events,
        team_name
    )

    # Keep strong connections only
    pass_network = pass_network[
        pass_network['pass_count'] >= 8
    ]

    pitch = Pitch(
        pitch_type='statsbomb',
        pitch_color='#1B4332',
        line_color='white',
        linewidth=2
    )

    fig, ax = pitch.draw(
        figsize=(14, 9)
    )

    # Draw pass links
    for _, row in pass_network.iterrows():

        passer = row['passer']
        recipient = row['recipient']

        passer_pos = avg_positions[
            avg_positions['player'] == passer
        ]

        recipient_pos = avg_positions[
            avg_positions['player'] == recipient
        ]

        if len(passer_pos) == 0 or len(recipient_pos) == 0:
            continue

        x1 = passer_pos['avg_x'].iloc[0]
        y1 = passer_pos['avg_y'].iloc[0]

        x2 = recipient_pos['avg_x'].iloc[0]
        y2 = recipient_pos['avg_y'].iloc[0]

        pitch.lines(
            x1,
            y1,
            x2,
            y2,
            lw=row['pass_count'] / 3,
            color='#ffb703',
            alpha=0.7,
            ax=ax
        )

    # Draw players
    pitch.scatter(
        avg_positions['avg_x'],
        avg_positions['avg_y'],
        s=avg_positions['touches'] * 8,
        color='#d00000',
        edgecolors='white',
        linewidth=2,
        ax=ax
    )

    # Names inside circles
    for _, row in avg_positions.iterrows():

        ax.text(
            row['avg_x'],
            row['avg_y'],
            format_player_name(row['player']),
            ha='center',
            va='center',
            color='white',
            fontsize=8,
            fontweight='bold'
        )

    ax.set_title(
        f'{team_name} Passing Network',
        fontsize=20,
        color='white',
        fontweight='bold',
        pad=20
    )

    fig.set_facecolor('#1B4332')

    return fig