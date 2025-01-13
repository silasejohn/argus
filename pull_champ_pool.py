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

position_list = ["top", "jng", "mid", "bot", "sup"]
ign = "Atamaex#NA1"
pos = "top"
pull_champ_pool(ign, pos)