import csv
from collections import defaultdict

def create_player_game_dict(filename):
    # Use defaultdict to automatically initialize lists for new player IDs
    player_game_dict = defaultdict(list)
    
    # Open the CSV file and read its contents
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)  # Use DictReader to access columns by name
        
        for row in reader:
            player_id = row['PLAYER_ID']
            game_id = row['GAME_ID']
            
            # Append game_id to the list for each unique player_id
            player_game_dict[player_id].append(game_id)
    
    return dict(player_game_dict)  # Convert defaultdict to a regular dictionary


def get_team_ids_from_csv(filename):
    # Use defaultdict to automatically initialize lists for new player IDs
    team_ids = []
    # Open the CSV file and read its contents
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)  # Use DictReader to access columns by name
        
        for row in reader:
            team_id = row['id']
            
            # Append game_id to the list for each unique player_id
            team_ids.append(team_id)
    
    return team_ids  # Convert defaultdict to a regular dictionary


def get_player_ids_from_csv(filename):
    # Use defaultdict to automatically initialize lists for new player IDs
    player_ids = []
    # Open the CSV file and read its contents
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)  # Use DictReader to access columns by name
        
        for row in reader:
            player_id = row['PLAYER_ID']
            
            # Append game_id to the list for each unique player_id
            player_ids.append(player_id)
    
    return player_ids  # Convert defaultdict to a regular dictionary



def get_game_ids_from_csv(filename):
    # Use defaultdict to automatically initialize lists for new player IDs
    game_ids = []
    # Open the CSV file and read its contents
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)  # Use DictReader to access columns by name
        
        for row in reader:
            game_id = row['GAME_ID']
            
            # Append game_id to the list for each unique player_id
            game_ids.append(game_id)
    
    return list(set(game_ids))   # Convert defaultdict to a regular dictionary

# Usage example
teams_game_logs_filename = "./data/teams_game_logs.csv"
game_ids = get_game_ids_from_csv(teams_game_logs_filename)
print(game_ids)