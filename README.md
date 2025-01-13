# A Draft Analysis Tool

This project aims to provide a toolset to analyze sign-up responses for VLN Draft S1. This should help our team captain prioritize potential players based on specific criteria such as role preference, rank, and champ pool. 

## Features
**Profile Geneneration**: Create and Automatically Update multiple Player Draft Profiles
**Web Scraping**: Scrape multiple popular LoL Stat Websites for relevant and updated player information
**Role Analysis**: Identify player primary and secondary roles given a match history
**Rank Analysis**: Ascertain player true and peak rank potential 
**Draft Simulation**: Run sample, locally-optimized simulations of player drafts (tournament openers), filtering + ranking players in a skill-based manner
**Information Processing**: process any pre-tournament or sign-up data from input spreadsheets

## Getting Started

### Prereqs
- Python 3.7+
- Required Python packages (install via `requirements.txt`)
    - `pandas`
    - `sys`

### Installation
1. Clone this repository: 
    ```
    git clone git@github.com:silasejohn/VLN-Draft-Analysis.git
    ```

2. Install dependencies: 
    ```
    pip install -r requirements.txt
    ```
3. Place the updated sign-up response spreadsheet (`data.csv`) in the data/ folder

### Usage
1. Run the format script to format the csv
    ```
    python format.py
    ```
2. Run the analysis script to analyze the csv
     ```
    python analyze.py
    ```
3. Export / Run Locally to Visualize Results
4. Use the "draft tool" to maintain priorities on players left in draft

## Customization / Config
....

## Acknowledgments
Special thanks to GepettosPuppet 

### Other
Create Virtual Environment: `python3.9 -m venv [name]-env`
Activate Virtual Environment: `source [name]-env/bin/activate`
Install Dependency List: `pip3 install -r requirements.txt`
Deactivate Virtual Environment: `deactivate`

#### TODO
1. look through raw spreadsheet + read qualitative descriptions ~> assign a bool value of "consideration"
2. look through primary / secondary rank descriptions ~> assign a bool value of "consider_secondary_role"
3. create selenium scripts for op.gg champ history, and rewind.lol to access more quantitative scouting info
4. COOL PRINT OUTPUT + DYNAMIC PRINT OUTPUT
5. TODO: change examples / test into pyunit or whatnot
6. Build Local React App ~> Live Draft Tool for Gepetto during Draft
7. Add Region Button Press for NA (when switching regions) handling incorrect input
8. Consider Friend Pools in draft picking
9. TAB the output for draft results
10. determine the number of games for a given rank (in the rank_output csv)
11. get wr / champs played / per mode per player (combine accounts, seperate accounts) ... try rewind.lol?
12. Look at chart for potential cap recruitments
13. live draft dashbaord (look pic of inspo)
14. Easy to Input Profiles + Suspected Roles ~> Automated Full Profile per Person (via GoogleSpreadsheets)
15. make sure that local storage of rewind.lol champs categorizes into proper buckets
