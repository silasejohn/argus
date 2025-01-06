import sys
import json
import pandas as pd
import utility as util

""" CAPTAIN INFO
Cheese (Top)        ... mrlizwiz
Earthen (Top)       ... earthen
VLN (top lane)      ... verylastnerve
Vowels (top lane)   ... .f_g.

Hello Kitty!@ (Jungle i think)  ... recoveringschizo
Lakuna (Jungle)                 ... _lakuna
acekiller1107 (Jungle)          ... axekiller1107

Morgana, My Beloved (Mid)   ... catinatin
Lapiz Lazuli (Mid)          ... lapislazuli3824
NAQI (Mid)                  ... ffsfruit

Different (ADC)     ... different_lol
Stran (ADC)         ... .stran
Team Curse (ADC)    ... aratthe
Peepa (ADC)         ... jayrich1101
Stl Slayer (ADC)    ... stl_slayer_24

DavidEdge (Support) ... davidedge
"""

MAX_PLAYERS_PER_TEAM = 8
ROLES = ['ADC', 'Mid', 'Jungle', 'Support', 'Top']

### captains as in order for pick order
captains = ['VeryLastNerve',
            '_lakuna',
            '.stran',
            'mrlizwiz',
            'Lapislazuli3824',
            'Earthen',
            '.f_g.',
            'recoveringschizo',
            'jayrich1101', 
            'ffsfruit',
            'different_lol',
            'Stl_Slayer_24',
            'DavidEdge', 
            'catinatin', 
            'axekiller1107',
            'aratthe']

# open draft info spreadsheet as pandas df
draft_pool_df = pd.read_csv('data/simulation_data_with_points.csv')
draft_pool_df = draft_pool_df.drop(columns=['opgg_link', 'peak_rank_explanation', 'availability', 'interest_in_captain', 'reference_to_vln_league', 'playstyle_description', 'join_discord_flag', 'is_peak_rank_true_rank', 'champion_identity', 'secondary_role_skill_level'])

# print all unique 'discord_username' values
print(draft_pool_df['discord_username'].unique())

# create new df with only rows of captains that are in 'discord_username' column ... 'cap_df'
cap_df = pd.DataFrame(columns=draft_pool_df.columns)
for captain in captains:
    cap_df = pd.concat([cap_df, draft_pool_df[draft_pool_df['discord_username'] == captain]], ignore_index=True)
cap_draft_ordered_df = cap_df.sort_values(by=['rank_score'], ascending=True).reset_index(drop=True)

# create a df with no captain in it 'draft_df'
draft_df = draft_pool_df[~draft_pool_df['discord_username'].isin(captains)]
draft_df = draft_df.sort_values(by='rank_score', ascending=True).reset_index(drop=True) # sort draft pool by rank
players_pool = draft_df.copy()

# export player draft pool and cap draft pool in pretty print to a text file
with open('data/player_draft_pool.txt', 'w') as file:
    line_idx = 0 # every 16 players, draw a line
    player_idx = 1
    file.write("=== Player Draft Pool ===\n")
    # sort by rank
    players_pool = players_pool.sort_values(by=['rank_score'], ascending=True)
    for index, row in players_pool.iterrows():
        file.write(f"[{player_idx}] {row['discord_username']} - {row['peak_rank_2024_split3']} ({row['primary_role']}) - {row['rank_score']}\n")
        if player_idx % 16 == 0:
            file.write(f"--- END DRAFT PERIOD {line_idx + 1} ---\n")
            line_idx += 1
        player_idx += 1

# export player draft pool by role to 5 more text files
role_pool_df = pd.read_csv('data/simulation_data_with_points.csv')
role_pool_df = role_pool_df.drop(columns=['opgg_link', 'peak_rank_explanation', 'availability', 'interest_in_captain', 'reference_to_vln_league', 'playstyle_description', 'join_discord_flag', 'is_peak_rank_true_rank', 'champion_identity'])
role_pool_df = role_pool_df[~role_pool_df['discord_username'].isin(captains)]
role_pool_df = role_pool_df.sort_values(by='rank_score', ascending=True).reset_index(drop=True) # sort draft pool by rank
for role in ROLES:
    with open(f'data/{role}_player_draft_pool.txt', 'w') as file:
        total_points = 0
        total_entries = 0

        player_idx = 1
        file.write(f"=== Player Draft Pool ({role}) ===\n")
        
        # filter by role

        # print role pool df size
        # print(f"role_pool_df: {role_pool_df.shape}")
        players_pool_filtered_by_role = role_pool_df[role_pool_df['primary_role'] == role]
        # print(f"role_pool_df: {role_pool_df.shape}")
        # sys.exit()
        
        # create df subset player_pool_2 if players_pool['secondary_role'] == role as long as players_pool['secondary_role_skill_level'] == "Equal"
        players_pool_2 = role_pool_df[role_pool_df['secondary_role'] == role]
        players_pool_2 = players_pool_2[players_pool_2['secondary_role_skill_level'] == "Equal"]
        
        # in players_pool_2 replace 'primary_role' with 'secondary_role'
        players_pool_2['primary_role'] = players_pool_2['secondary_role']

        # concat players_pool_filtered_by_role and players_pool_2
        players_pool_filtered_by_role = pd.concat([players_pool_filtered_by_role, players_pool_2], ignore_index=True)

        # sort by rank
        players_pool_filtered_by_role = players_pool_filtered_by_role.sort_values(by=['rank_score'], ascending=True)

        for index, row in players_pool_filtered_by_role.iterrows():
            if pd.notna(row['rank_score']):
               total_points += row['rank_score']
            total_entries += 1
            file.write(f"[{player_idx}] {row['discord_username']} - {row['peak_rank_2024_split3']} ({row['primary_role']}) - {row['rank_score']}\n")
            player_idx += 1
        
        file.write(f"\n\nTotal Entries: {total_entries}")
        file.write(f"\nAverage Points ({role}): {total_points / total_entries}")
        

with open('data/cap_draft_pool.txt', 'w') as file:
    cap_idx = 1
    file.write("=== Captain Draft Pool ===\n")
    for index, row in cap_df.iterrows():
        file.write(f"[{cap_idx}] {row['discord_username']} - {row['peak_rank_2024_split3']} ({row['primary_role']}) - {row['rank_score']}\n")
        cap_idx += 1
    cap_idx = 1
    file.write(f"\n\n=== Captain Draft Pool (Ordered) ===\n")
    for index, row in cap_draft_ordered_df.iterrows():
        file.write(f"[{cap_idx}] {row['discord_username']} - {row['peak_rank_2024_split3']} ({row['primary_role']}) - {row['rank_score']}\n")
        cap_idx += 1

# print(cap_df)
# print(draft_df)
# sys.exit()

############################################################################################################
############################################################################################################
############################################################################################################

# run a simulation
from collections import defaultdict

# init a potential draft dictionary
draft_results = defaultdict(list)

# simulate the snake draft
# snake_order = list(range(len(cap_df))) + list(range(len(cap_df) - 1, -1, -1))
snake_order = (list(range(len(cap_df))) + list(range(len(cap_df) - 1, -1, -1))) * 3 + list(range(len(cap_df)))  
captains_list = cap_df.to_dict('records')

# add all captains as the first player in their respective teams
for captain in captains_list:
    draft_results[captain['discord_username']].append(captain)

# create an array of flags with # of indexs equal to number of captains
cap_flags = [0] * len(captains)

print(f"cap_flags: {cap_flags}")

def force_player_onto_team(pool, player, captain_id):
    pool = pool[pool['discord_username'] != player['discord_username']]
    draft_results[captain_id].append(player.to_dict())
    cap_flags[captains.index(captain_id)] += 1
    print(f"captains: {captain_id}")
    print(f"captains.index(captain_id): {captains.index(captain_id)}")
    print(f"cap_flags: {cap_flags}")
    return pool

# open a "in progress draft notes file"
with open('data/draft_in_progress.txt', 'w') as file:
    file.write("=== Draft In Progress ===\n")

    # force pick a player for a captain
    print(f"\n=== Force Pick ===")
    force_cap_1 = 'jayrich1101'
    force_player_pick_1 = 'Owen0214'
    players_pool = force_player_onto_team(players_pool, players_pool[players_pool['discord_username'] == force_player_pick_1].iloc[0], force_cap_1)

    for round_num in range(1, MAX_PLAYERS_PER_TEAM):
        print(f"\n=== Round {round_num} ===")
        file.write(f"\n=== Round {round_num} ===")
        snake_pick_count = 0 # represents what pick of the draft we are on
        snake_picks_left = 16 * 8 - 1 # represents how many picks have been made
        for pick_num_in_round in range(16): # represents the number of picks per round
            cap_idx = snake_order[snake_pick_count] # get the captain index
            snake_pick_count += 1 # increment the pick count
            snake_picks_left -= 1 # decrement the picks left
            captain = captains_list[cap_idx]
            captain_id = captain['discord_username']

            if cap_flags[captains.index(captain_id)] >= 1:
                print(f"{util.RED}Captain [{captain_id}] cannot pick. Already picked this round!{util.RESET}")
                cap_flags[captains.index(captain_id)] -= 1 # decrement the flag
                continue

            # if cap alr has MAX_PLAYERS_PER_TEAM then go next
            if len(draft_results[captain_id]) >= MAX_PLAYERS_PER_TEAM:
                continue

            # normal simulation 
            if round_num != 3 and round_num != 7:
                # determine a needed role
                drafted_roles = [player['primary_role'] for player in draft_results[captain_id]]
                needed_roles = [role for role in ROLES if role not in drafted_roles]

                # prio needed roles 
                if needed_roles:
                    eligible_player = players_pool[players_pool['primary_role'].isin(needed_roles)]
                else:
                    eligible_player = players_pool
            
            elif round_num == 3:
                # determine total point value from rank_score of all players currently on a team
                total_points = sum([player['rank_score'] for player in draft_results[captain_id]])
                print(f"{util.CYAN}Captain [{captain_id}] total points: {total_points}{util.RESET}")
                file.write(f"\nCaptain [{captain_id}] total points: {total_points}")

                # calculate difference from threshold of 80
                rank_difference = 80 - total_points

                # find players with rank_score higher or equal to than rank_difference
                eligible_player = players_pool[players_pool['rank_score'] >= rank_difference]

            elif round_num == 7:
                # determine total point value from rank_score of all players currently on a team
                total_points = sum([player['rank_score'] for player in draft_results[captain_id]])
                print(f"{util.CYAN}Captain [{captain_id}] total points: {total_points}{util.RESET}")
                file.write(f"\nCaptain [{captain_id}] total points: {total_points}")

                # calculate difference from threshold of 160
                rank_difference = 160 - total_points

                # find players with rank_score higher or equal to than rank_difference
                eligible_player = players_pool[players_pool['rank_score'] >= rank_difference]

            # sort by rank
            eligible_player = eligible_player.sort_values(by=['rank_score'], ascending=True)

            if eligible_player.empty:
                print(f"{util.RED}Captain [{captain_id}] cannot pick. No eligible players left!{util.RESET}")
                file.write(f"\nCaptain [{captain_id}] cannot pick. No eligible players left!")
                continue

            # how to handle ties
            top_rank_score = eligible_player.iloc[0]['rank_score']
            top_candidates = eligible_player[eligible_player['rank_score'] == top_rank_score]

            if len(top_candidates) > 1:
                print(f"{util.YELLOW}Tie for Captain [{captain_id}]: {top_candidates[['discord_username', 'primary_role']].to_dict('records')}{util.RESET}")
                file.write(f"\nTie for Captain [{captain_id}]: {top_candidates[['discord_username', 'primary_role']].to_dict('records')}")
                selected_player = top_candidates.iloc[0]
            else:
                selected_player = top_candidates.iloc[0]

            # add player to captains draft and remove from pool
            draft_results[captain_id].append(selected_player.to_dict())

            # remove player from the draft pool 
            players_pool = players_pool[players_pool['discord_username'] != selected_player['discord_username']]

            # [PRINT]
            print (f"{util.GREEN}Captain [{captain_id}] picked [{selected_player['discord_username']}] ({selected_player['primary_role']})!{util.RESET}")
            file.write (f"\nCaptain [{captain_id}] picked [{selected_player['discord_username']}] ({selected_player['primary_role']})!")

# pretty print the results
print("\n=== Final Draft Results ===")
for captain_id, team in draft_results.items():
    print(f"\n{util.CYAN}Captain [{captain_id}] Team:")
    # calculate total points
    total_points = sum([player['rank_score'] for player in team])
    print(f"\tTotal Points: {total_points}")  
    for player in team:
        print(f"{player['discord_username']} - {player['peak_rank_2024_split3']} ({player['primary_role']}) - {player['rank_score']}")

# output pretty print results into a .txt file in /data 
with open('data/draft_results.txt', 'w') as file:
    file.write("=== Final Draft Results ===\n")
    for captain_id, team in draft_results.items():
        file.write(f"\nCaptain [{captain_id}] Team:\n")     
        # calculate total points
        total_points = sum([player['rank_score'] for player in team])
        file.write(f"Total Points: {total_points}\n")   
        for player in team:
            file.write(f"{player['discord_username']} - {player['peak_rank_2024_split3']} ({player['primary_role']}) - {player['rank_score']}\n")

