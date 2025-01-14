import os
import sys
import pandas as pd

position_list = ["top", "jng", "mid", "bot", "sup"]

def pull_champ_pool(player_ign, pos):
    # check the data/rewind/output folder for any files starting with player_ign and print their names
    print("Files found for " + player_ign + ":")
    for file in os.listdir("data/rewind/output"):
        # and file ends with "pos.csv"
        if file.startswith(player_ign) and file.endswith(pos + ".csv"):
            # setup a df for this csv 
            df = pd.read_csv("data/rewind/output/" + file)

            # print full df itself
            print(df)

def pull_multiple_champ_pool(player_ign_list, player_pos_list):
    # player_ign_list is a list of players
    # player_pos_list is a list of positions where index of pos corresponds to index of ign, pos[i] has 1+ positions either as 'top' or 'top|jng|mid' if there are multiple positions per player
    for i in range(len(player_ign_list)):
        # split the pos[i] by '|' to get a list of positions
        pos_list = player_pos_list[i].split("|")
        for pos in pos_list:
            print(f"Pulling champ pool for {player_ign_list[i]} in {pos}")
            pull_champ_pool(player_ign_list[i], pos)

position_list = ["top", "jng", "mid", "bot", "sup"]

# ign = "Top Tower#NA1"
# pos = "top"
# pull_champ_pool(ign, pos)

team_ign_list = ["Top Tower#NA1", "I fear nobody#NA1", "Niccus#gopha", "it is what it is#na3", "Bound#WVU1", "Team Curse #NA1", "Proud In Shroud#MAD", "Feeshstix#fish"]
team_pos_list = ["top", "jng", "mid|bot", "bot|sup", "sup|top", "sup", "mid", "bot"]
pull_multiple_champ_pool(team_ign_list, team_pos_list)

# PeepaTheHound#Molly


# Initial Thoughts + Chapter 2