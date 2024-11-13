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

# Usage example
filename = "C:\\Users\\tg715c\\Documents\\Learning\\wnba-stats\\data\\player_game_logs.csv"
player_game_dict = create_player_game_dict(filename)
print(player_game_dict)