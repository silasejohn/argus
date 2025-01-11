##########################
### Import Statements ####
##########################

# data manipulation, time buffering, quick exit, csv editing
import pandas as pd
import time, sys, csv, os

# pretty printing and color
import utility as util

# Selenium WebDriver Options
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions    #  for FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions      # for ChromeOptions
from selenium.webdriver.firefox.service import Service                      # for FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService      # for ChromeService
from selenium.webdriver.common.by import By                                 # for locating elements BY specific types (e.g. ID, NAME, etc.)
from selenium.webdriver.common.keys import Keys                             # for clicking RETURN
from selenium.webdriver.support.ui import Select                            # for dropdown menus (element selection)
from selenium.webdriver.support.ui import WebDriverWait                     # for waiting for elements to load
from selenium.webdriver.support import expected_conditions as EC            # for expected conditions
from selenium.common.exceptions import TimeoutException, NoSuchElementException     # for timeout exceptions

def argus_print(msg):
    print(f"\n[[{util.MAGENTA} a r g u s {util.RESET}]] >> {msg}...")

def create_data_df(csv_file):
    data_df = pd.read_csv(csv_file)
    return data_df

#######################################
### LeagueChampScraper (rewind.lol) ###
#######################################
class LeagueChampScraper:

    MAIN_WEBSITE = 'https://rewind.lol/'
    DRIVER = None
    BROWSER = "chrome"
    WEBSITE_TIMEOUT = 5

    ROLE_ACRYONYMS = {  
        "Top": "top",
        "Jungle": "jng",
        "Mid": "mid",
        "Bot": "bot",
        "Support": "sup"
    }

    CHAMPS_IN_ROLES = {
        "Ahri": "mid",
        "Akali": "mid",
        "Alistar": "sup",
        "Amumu": "jng",
        "Anivia": "mid",
        "Annie": "mid",
        "Aphelios": "bot",
        "Ashe": "bot",
        "Aurelion Sol": "mid",
        "Azir": "mid",
        "Bard": "sup",
        "Blitzcrank": "sup",
        "Brand": "sup",
        "Braum": "sup",
        "Caitlyn": "bot",
        "Camille": "top",
        "Cassiopeia": "mid",
        "Cho'Gath": "top",
        "Corki": "mid",
        "Darius": "top",
        "Diana": "mid",
        "Dr. Mundo": "top",
        "Draven": "bot",
        "Ekko": "mid",
        "Elise": "jng",
        "Evelynn": "jng",
        "Ezreal": "bot",
        "Fiddlesticks": "jng",
        "Fiora": "top",
        "Fizz": "mid",
        "Galio": "mid",
        "Gangplank": "top",
        "Garen": "top",
        "Gnar": "top",
        "Gragas": "top",
        "Graves": "jng",
        "Hecarim": "jng",
        "Heimerdinger": "mid",
        "Illaoi": "top",
        "Irelia": "top",
        "Ivern": "jng",
        "Janna": "sup",
        "Jarvan IV": "jng",
        "Jax": "top",
        "Jayce": "top",
        "Jhin": "bot",
        "Jinx": "bot",
        "Kai'Sa": "bot",
        "Kalista": "bot",
        "Karma": "sup",
        "Karthus": "jng",
        "Kassadin": "mid",
        "Katarina": "mid",
        "Kayle": "top",
        "Kayn": "jng",
        "Kennen": "top",
        "Kha'Zix": "jng",
        "Kindred": "jng",
        "Kled": "top",
        "Kog'Maw": "bot",
        "LeBlanc": "mid",
        "Lee Sin": "jng",
        "Leona": "sup",
        "Lillia": "jng",
        "Lissandra": "mid",
        "Lucian": "bot",
        "Lulu": "sup",
        "Lux": "sup",
        "Malphite": "top",
        "Malzahar": "mid",
        "Maokai": "top",
        "Master Yi": "jng",
        "Miss Fortune": "bot",
        "Mordekaiser": "top",
        "Morgana": "sup",
        "Nami": "sup",
        "Nasus": "top",
        "Nautilus": "sup",
        "Neeko": "mid",
        "Nidalee": "jng",
        "Nocturne": "jng",
        "Nunu & Willump": "jng",    
        "Olaf": "top",
        "Orianna": "mid",
        "Ornn": "top",
        "Pantheon": "top",
        "Poppy": "top",
        "Pyke": "sup",
        "Qiyana": "mid",
        "Quinn": "top",
        "Rakan": "sup",
        "Rammus": "jng",
        "Rek'Sai": "jng",
        "Rell": "sup",
        "Renekton": "top",
        "Rengar": "jng",
        "Riven": "top",
        "Rumble": "top",
        "Ryze": "mid",
        "Samira": "bot",
        "Sejuani": "jng",
        "Senna": "bot",
        "Seraphine": "mid",
        "Sett": "top",
        "Shaco": "jng",
        "Shen": "top",
        "Shyvana": "jng",
        "Singed": "top",
        "Sion": "top",
        "Sivir": "bot",
        "Skarner": "jng",
        "Sona": "sup",
        "Soraka": "sup",
        "Swain": "mid",
        "Sylas": "mid",
        "Syndra": "mid",
        "Tahm Kench": "sup",
        "Taliyah": "mid",   
        "Talon": "mid",
        "Taric": "sup",
        "Teemo": "top",
        "Thresh": "sup",
        "Tristana": "bot",
        "Trundle": "jng",
        "Tryndamere": "top",
        "Twisted Fate": "mid",
        "Twitch": "bot",
        "Udyr": "jng",
        "Urgot": "top",
        "Varus": "bot",
        "Vayne": "bot",
        "Veigar": "mid",
        "Vel'Koz": "mid",
        "Vi": "jng",
        "Viego": "jng",
        "Viktor": "mid",
        "Vladimir": "mid",
        "Volibear": "jng",
        "Warwick": "jng",
        "Wukong": "jng",
        "Xayah": "bot",
        "Xerath": "mid",
        "Xin Zhao": "jng",
        "Yasuo": "mid",
        "Yone": "mid",
        "Yorick": "top",
        "Yuumi": "sup",
        "Zac": "jng",
        "Zed": "mid",
        "Ziggs": "mid",
        "Zilean": "mid",
        "Zoe": "mid",
        "Zyra": "sup"
    }
        
    @staticmethod
    # sets up the rewind.lol website
    def set_up_rewind_lol():
        try: 
            argus_print("Prepping Rewind.lol")
            LeagueChampScraper.get_web_driver()
            LeagueChampScraper.DRIVER.get(LeagueChampScraper.MAIN_WEBSITE)
            return 1 # success
        except Exception as e:
            print(f"Error: {e}")
            LeagueChampScraper.close()
            return -1 # error
        
    @staticmethod
    # enter in player IGN and arrive at their rewind.lol profile page
    def load_player_profile(player_ign):
        argus_print(f"Entering Player IGN: {player_ign}")
        try:
            status = LeagueChampScraper.select_region()

            # Find the rewind.lol search box, enter player IGN, and hit Enter
            search_box = LeagueChampScraper.DRIVER.find_element(By.CLASS_NAME, 'main__interface-menu-input')
            search_box.send_keys(player_ign + Keys.RETURN)  # Send query and hit Enter

            return 1 # success
        except Exception as e:
            print(f"Error: {e}")
            return -1 # error
    
    @staticmethod
    # waits for an "element" to show up on page
    # used to wait for page (and specific element) to load
    def wait_for_element_to_load(by, value, timeout=10, custom_error_msg=None):
        try:
            element = WebDriverWait(LeagueChampScraper.DRIVER, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            if custom_error_msg:
                print(f"{util.RED}{custom_error_msg}{util.RESET}")
            else:
                print(f"{util.RED}{value} Element not Found!{util.RESET}")
            return -1
    
    @staticmethod
    # access player's champion history
    def access_player_champion_history():
        argus_print("Accessing Player Champion History")
        try:
            # Find the Champion History Button and Click
            champ_history_menu = LeagueChampScraper.DRIVER.find_element(By.XPATH, "//a[contains(@onclick, '/user_champions.html')]")
            champ_history_menu.click()  # Click the element

        except Exception as e:
            print(f"{util.RED}[ERROR] Error accessing player champion history: {e}{util.RESET}")

    @staticmethod
    # access player champion history table
    def access_player_champion_history_table(player_ign, file_name, role_prio_list):
        argus_print(f"Accessing {player_ign} Champion History Table")
        try:
            # Test: Find the Champion History Table
            LeagueChampScraper.wait_for_element_to_load(By.XPATH, "//*[text()='Champions Played and stats for PvP games']")
            champ_history_header = LeagueChampScraper.DRIVER.find_element(By.XPATH, "//*[text()='Champions Played and stats for PvP games']")

            # Find a title element from header row
            LeagueChampScraper.wait_for_element_to_load(By.XPATH, "//th[contains(@title, 'total KDA')]")
            element = LeagueChampScraper.DRIVER.find_element(By.XPATH, "//th[contains(@title, 'total KDA')]")

            # Find Header Row
            header_row = element.find_element(By.XPATH, "parent::*")
            # print(f"{util.YELLOW}Header: {header_row.text}{util.RESET}")

            # Find Main Table of Data
            champ_history_table_tbody = header_row.find_element(By.XPATH, "parent::*")

            # store all the <tr> rows in this tbdoy element champ_history_table_tbody
            tr_elements = champ_history_table_tbody.find_elements(By.TAG_NAME, 'tr')

            # Extract Header Row from Table
            header_row = tr_elements[0].find_elements(By.TAG_NAME, 'th')
            # print(f"{util.YELLOW}# of Headers: {len(header_row)}{util.RESET}")

            # Extract Data Rows from Table
            data_rows = tr_elements[1:]

            # Write to CSV File
            role_prio_entry = []
            with open(file_name, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if header_row: # write headers
                    writer.writerow([header.text.strip().replace("\n"," ") for header in header_row])
                else: # If there are no 'th' tags, use the first row as headers
                    first_row = data_rows[0].find_elements(By.TAG_NAME, 'td')
                    writer.writerow([cell.text for cell in first_row])

                for row in data_rows: # Write the rows to the CSV file (each tr is a row)
                    cells = row.find_elements(By.TAG_NAME, 'td')
                    
                    if cells:  # Skip rows without 'td' elements
                        row_data = []
                        
                        first_cell = True
                        for cell in cells:
                            if first_cell:
                                try:
                                    img_src_text = cells[0].find_element(By.TAG_NAME, 'span').find_element(By.TAG_NAME, 'img').get_attribute('src')
                                    role = img_src_text.split('/')[-1].split('.webp')[0]
                                    # print(f"{util.YELLOW}Position: {role}{util.RESET}")
                                    new_cell_text = cells[0].text + f" ({role})"
                                    row_data.append(new_cell_text.strip())
                                except NoSuchElementException:
                                    # if the text has a "_" in it, then it is a champion name
                                    if "_" in cells[0].text:
                                        new_cell_text = cells[0].text.replace("_", "[Role] ").strip()
                                        role_prio_entry.append(cells[0].text.replace("_", "").strip())
                                        row_data.append(new_cell_text)
                                    else:
                                        row_data.append(cells[0].text.strip())
                                first_cell = False
                            else:
                                row_data.append(cell.text.strip())
                        writer.writerow(row_data)
                role_prio_msg = f"[{player_ign}] Role Priority List (past 2 years): {role_prio_entry}"
                role_prio_list.append(role_prio_msg)
                print(f"{util.CYAN}{role_prio_msg}{util.RESET}")

            # import the csv back into a dataframe
            print(f"{util.YELLOW}Refining CSV File: {file_name}{util.RESET}")
            champ_df = pd.read_csv(file_name, sep=',')

            # loop through each row in the dataframe
            print(f"{util.YELLOW}Extracting Roles from Champion Names{util.RESET}")
            for index, row in champ_df.iterrows():
                champ_name = row['champion']
                # if the champ_name has [Role] in it, output 'Overview' in the 'Role' column
                # print(f"{util.YELLOW}Champion: {champ_name}{util.RESET}")
                if champ_name.find("[Role]") != -1:
                    champ_df.at[index, 'role'] = "OVERVIEW"
                # if the champ_name has parenthesis in it, extract the role from the parenthesis into the 'Role' column
                elif champ_name.find("(") != -1:
                    champ_df.at[index, 'role'] = champ_name.split("(")[1].split(")")[0]
                else: # if the champ_name is a champion name, extract the role from the CHAMPS_IN_ROLES dictionary
                    # champ_df.at[index, 'role'] = LeagueChampScraper.CHAMPS_IN_ROLES[champ_name]
                    pass
            file_name = file_name.replace("_raw.csv", "") # strip .csv from file_name
            file_name = file_name + "_refined.csv" # add "_refined.csv" to file_name
            champ_df.to_csv(file_name, index=False) # save to new csv file

            ### Role by Role df ### 
            # for each role of [top, jng, mid, bot, sup, OVERVIEW], create a new df and save to csv
            for role in ['top', 'jng', 'mid', 'bot', 'sup', 'OVERVIEW', '']:
                role_df = champ_df[champ_df['role'] == role]
                if not role_df.empty:
                    if role == '':
                        role_df.to_csv(file_name.replace("_refined.csv", f"_leftovers.csv"), index=False)
                    elif role == 'OVERVIEW':
                        role_df.to_csv(file_name.replace("_refined.csv", f"_role_distribution.csv"), index=False)
                    else:
                        role_df.to_csv(file_name.replace("_refined.csv", f"_{role}.csv"), index=False)
            return role_prio_list
        except Exception as e:
            print(f"{util.RED}[ERROR] Error accessing player champion history table: {e}{util.RESET}")
            return role_prio_list

    @staticmethod
    # access player's champion history for a single champion
    def access_single_champion_history(player_name, champion_name):

        # make champion_name CamelCase
        champion_name = champion_name.lower().title()

        argus_print(f"Accessing Player Champion History for <{champion_name}>")
        try:
            # Find the Champion History Button and Click
            champ_select_element = LeagueChampScraper.DRIVER.find_element(By.ID, 'd1f-champion-name')

            # Click the element
            champ_select_element.click()

            # Wrap the element in a Select object
            champ_select = Select(champ_select_element)

            # Select an option by value (e.g., 'NA' for North America)
            # 3 options: select_by_index, select_by_value, select_by_visible_text
            champ_select.select_by_visible_text(champion_name)

            # click
            champ_select_element.click()

            return 1 # success

        except Exception as e:
            print(f"{util.RED}[ERROR] Error accessing player champion history for {champion_name}: {e}{util.RESET}")
            return -1 # error

    @staticmethod
    # selection of region NA
    def select_region(region = 'NA'):
        argus_print(f"Selecting Region: {region}")
        try:
            # Find the Region Select Dropdown
            region_select_element = LeagueChampScraper.DRIVER.find_element(By.CLASS_NAME, 'main__interface-menu-input-servers')

            # Wrap the element in a Select object
            region_select = Select(region_select_element)

            # Select an option by value (e.g., 'NA' for North America)
            region_select.select_by_value('NA')
            
            return 1 # success
        except Exception as e:
            print(f"{util.RED}[ERROR] Error selecting region {region}: {e}{util.RESET}")
            return -1 # error

    @staticmethod
    # sets up the webdriver (automated chrome access)
    # [returns] 1 if driver created, 0 if driver already exists
    def get_web_driver():
        if LeagueChampScraper.DRIVER is None:
            argus_print("Setting up Chrome WebDriver")
            if LeagueChampScraper.BROWSER.lower() == "firefox":
                options = FirefoxOptions()
                options.headless = True  # Runs in headless mode, no UI.
                service = Service('/path/to/geckodriver')  # Path to geckodriver
                LeagueChampScraper.DRIVER = webdriver.Firefox(service=service, options=options)
            elif LeagueChampScraper.BROWSER.lower() == "chrome":
                options = ChromeOptions()
                options.headless = True  # Runs in headless mode, no UI.
                service = ChromeService('/opt/homebrew/bin/chromedriver')  # Path to chromedriver
                LeagueChampScraper.DRIVER = webdriver.Chrome(service=service, options=options)
            else:
                raise ValueError("Only 'firefox' and 'chrome' browsers are supported.")
            return 1 # driver created
        else:
            return 0 # driver already exists
    
    @staticmethod
    def process():
        pass

    def buffer(time_sec = WEBSITE_TIMEOUT):
        time.sleep(time_sec)

    @staticmethod
    def close():
        LeagueChampScraper.DRIVER.quit()

    @staticmethod   
    def close_previous_tab():
        # Get a list of all open tabs
        tabs = LeagueChampScraper.DRIVER.window_handles

        # Switch to the previous tab
        LeagueChampScraper.DRIVER.switch_to.window(tabs[0])

        # Close the Current Tab
        LeagueChampScraper.DRIVER.close()

        # Switch to the previous tab open
        LeagueChampScraper.DRIVER.switch_to.window(tabs[-1]) # tabs[-1] is the last tab opened 

    @staticmethod
    def create_new_tab():
        # # Open a new tab
        # LeagueChampScraper.DRIVER.execute_script("window.open('');")

        # # Switch to the new tab
        # LeagueChampScraper.DRIVER.switch_to.window(LeagueChampScraper.DRIVER.window_handles[-1])

        # Load a new instance of rewind.lol in new tab
        LeagueChampScraper.DRIVER.execute_script("window.open('https://rewind.lol', '_blank');")


###################
### DRIVER CODE ###
###################

# go to data/rewind/output directory and find all the csvs that end in _role_distribution.csv
# for each csv, read the csv and extract the role distribution

# create a new df with 'profile_ign', 'primary_role', 'primary_role_games', 'primary_role_winrate', 'secondary_role', 'secondary_role_games', 'secondary_role_winrate'
role_df = pd.DataFrame(columns=['profile_ign', 'primary_role', 'primary_role_games', 'primary_role_winrate', 'secondary_role', 'secondary_role_games', 'secondary_role_winrate', 'rank_score'])

for file in os.listdir("data/rewind/output"):
    if file.endswith("_role_distribution.csv"):
        role_dist_df = pd.read_csv(f"data/rewind/output/{file}")
        profile_ign = file.replace("_role_distribution.csv", "")
        # extract 'champion' and 'total games' and 'winrate' columns
        role_dist_df = role_dist_df[['champion', 'total games', 'winrate']]

        # determine primary role by first row
        primary_role = role_dist_df.iloc[0]['champion'].replace("[Role] ", "")
        secondary_role = role_dist_df.iloc[1]['champion'].replace("[Role] ", "")
        primary_role_games = role_dist_df.iloc[0]['total games']
        primary_role_winrate = role_dist_df.iloc[0]['winrate']
        secondary_role_games = role_dist_df.iloc[1]['total games']
        secondary_role_winrate = role_dist_df.iloc[1]['winrate']

        # add to the role_df but don't use append
        new_data = {
            'profile_ign': profile_ign,
            'primary_role': primary_role,
            'primary_role_games': primary_role_games,
            'primary_role_winrate': primary_role_winrate,
            'secondary_role': secondary_role,
            'secondary_role_games': secondary_role_games,
            'secondary_role_winrate': secondary_role_winrate
        }

        new_row = pd.DataFrame([new_data])
        role_df = pd.concat([role_df, new_row], ignore_index=True)

# save role_df to csv
role_df.to_csv("data/rewind/role_df.csv", index=False)

# pull the input_data.csv and iterate through each row, for each profile ign save the rank score to the role_df
input_data_file = 'data/rewind/input_data.csv'
input_data_df = pd.read_csv(input_data_file)
role_df = pd.read_csv("data/rewind/role_df.csv")

# iterate through each row in the input_data_df
for index, row in input_data_df.iterrows():
    
    profile_ign = row['Summoner IGN']
    rank_score = row['Rank Score']
    positions = row['Pos']
    
    profile_ign_list = []
    position_list = []

    if "|" in positions:
        position_list = positions.split("|")
    else:
        position_list.append(positions)
    
    # replace all instances of "ADC" in position list with "Bot"
    position_list = [position.replace("ADC", "Bot") for position in position_list]
    
    if "|" in profile_ign:
        profile_ign_list = profile_ign.split("|")
    else:
        profile_ign_list.append(profile_ign)

    profile_ign_list = [ign.strip() for ign in profile_ign_list]

    for profile in profile_ign_list:
        if profile == "" or profile == "ICarryOrILose#FREAK" or profile == "Rose#630":
            continue # skip empty rows / invalid IGNs

        # print(f"Rank Score: {rank_score} for profile IGN: {profile}")
        profile_ign = profile
        role_row = role_df[role_df['profile_ign'] == profile_ign]
        if role_row.empty:
            print(f"Profile IGN {profile_ign} not found in role_df")
            continue
        role_df.at[role_row.index[0], 'rank_score'] = rank_score

        # check that the primary role is in the position_list
        primary_role = role_row['primary_role'].values[0]
        secondary_role = role_row['secondary_role'].values[0]

        if primary_role not in position_list:
            print (f"Primary Role {primary_role} not in Position List {position_list} for Profile IGN {profile_ign}")
        
        # check any role in the position_list that is not [0] as being a secondary role
        for position in position_list:
            if position != primary_role:
                if position != secondary_role:
                    print(f"Secondary Role {position} not in Secondary Role {secondary_role} for Profile IGN {profile_ign}")


role_df = role_df.sort_values(by='rank_score', ascending=True) # sort role_df by rank_score
role_df.to_csv("data/rewind/role_df.csv", index=False) # save role_df to csv
sys.exit()


input_data_file = 'data/rewind/input_data.csv'
draft_pool_df = create_data_df(input_data_file)
print(draft_pool_df)

# iterate through each row in the draft pool
setup = False
execute = False
role_prio_list = []
for index, row in draft_pool_df.iterrows():

    # obtain clean profile_igns
    profile_ign = row['Summoner IGN']

    if profile_ign == "" or profile_ign == "ICarryOrILose#FREAK": 
        continue # skip empty rows / invalid IGNs

    profile_ign_list = []
    if "|" in profile_ign:
        profile_ign_list = profile_ign.split("|")
    else:
        profile_ign_list.append(profile_ign)
    profile_ign_list = [ign.strip() for ign in profile_ign_list]

    # setup the rewind.lol website for scraping as needed
    if not setup:
        LeagueChampScraper.set_up_rewind_lol()
        setup = True

    # iterate through each profile_ign in the list
    for profile_ign in profile_ign_list:
        # only scrape the following profiles
        positive_profiles = ['Akatsuki37046#NA1']
        if profile_ign not in positive_profiles:
            continue

        LeagueChampScraper.load_player_profile(profile_ign)
        LeagueChampScraper.access_player_champion_history()
        champ_history_output = f"data/rewind/output/{profile_ign}_raw.csv"
        role_prio_list = LeagueChampScraper.access_player_champion_history_table(profile_ign, champ_history_output, role_prio_list)

        LeagueChampScraper.buffer()
        LeagueChampScraper.create_new_tab()
        LeagueChampScraper.close_previous_tab()

# add role_prio_list to txt file
counter = 0
with open("data/rewind/output/role_prio_list.txt", "w") as file:
    for role_list in role_prio_list:
        file.write(f"[{counter}] {role_list}\n")
        counter += 1

LeagueChampScraper.close()






