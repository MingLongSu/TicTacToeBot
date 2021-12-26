import json
import random

from discord import player

# gets the ttt channel
def get_ttt_channel(guild_id):
    with open('./data/all_guilds.json', 'r') as file:
        all_guild_data=json.load(file)

    return all_guild_data[f'{ guild_id }']['ttt_channel']

# gets the ttt queue data
def get_queue_data():
    with open('./data/player_queue.json', 'r') as file:
        queue_data=json.load(file)

    return queue_data

# overwrites the queue data with whatever passed changes
def overwrite_queue_data(queue_data):
    with open('./data/player_queue.json', 'w') as file:
        json.dump(queue_data, file, indent=len(queue_data))

# initialises the queue of players in TTT
def initialise_queue(user_id):
    queue_data = get_queue_data()

    if (f'{ user_id }' not in queue_data):
        queue_data[f'{ user_id }']={}
        queue_data[f'{ user_id }']['enqueue_pointer']=-1
        queue_data[f'{ user_id }']['dequeue_pointer']=0
        queue_data[f'{ user_id }']['queue']=list([None, None, None, None, None])

    # writing back to the queue file
    overwrite_queue_data(queue_data)

# checks if the queue of a player is full
def is_queue_full(p_id):
    queue_data = get_queue_data()

    return None not in queue_data[f'{ p_id }']['queue']

# checks if the requesting player is already in the queue of another player
def is_queue_spam(p1_id, p2_id):
    queue_data = get_queue_data()

    return p1_id in queue_data[f'{ p2_id }']['queue']

# checks if queue is empty: True when empty, False otherwise
def is_queue_empty(p_id):
    p_queue = get_queue_data()[f'{ p_id }']['queue']

    is_empty = True

    for player in p_queue:
        if (player != None):
            is_empty = False
            break
    
    return is_empty

# adds p1 to the queue of p2
def add_to_queue(p1_id, p2_id): 
    queue_data = get_queue_data()

    queue_data[f'{ p2_id }']['enqueue_pointer'] += 1
    ep = queue_data[f'{ p2_id }']['enqueue_pointer']
    queue_data[f'{ p2_id }']['queue'][ep % 5] = p1_id

    overwrite_queue_data(queue_data)

# removes the player on the dequeue pointer from the a queue list 
def delete_from_queue(p_id):
    queue_data = get_queue_data()

    dp = queue_data[f'{ p_id }']['dequeue_pointer']
    queue_data[f'{ p_id }']['queue'][dp % 5] = None
    queue_data[f'{ p_id }']['dequeue_pointer'] += 1

    overwrite_queue_data(queue_data)

# makes a queue display list
def make_queue_display(p_id):
    player_profile_data = get_player_profiles_data()
    queue_data = get_queue_data()
    dp = queue_data[f'{ p_id }']['dequeue_pointer']
    queue = queue_data[f'{ p_id }']['queue']

    display_queue_to_send = []

    def recurse_add(start, end, queue, display_queue): 
        if (queue[start % 5] != None): 
            curr_queued_player_id = queue[start % 5]
            curr_queued_payer_wins = player_profile_data[f'{ queue[start % 5] }']['wins']
            curr_queue_player_losses = player_profile_data[f'{ queue[start % 5] }']['losses']
            display_queue.append([curr_queued_player_id, curr_queued_payer_wins, curr_queue_player_losses])
        else:
            display_queue.append([queue[start % 5], 'N/A', 'N/A'])

        if (start % 5 == end):
            return display_queue
        else:
            start += 1
            return recurse_add(start, end, queue, display_queue)

    return recurse_add(dp, ((dp - 1) % 5), queue, display_queue_to_send)

# gets player profile data
def get_player_profiles_data():
    with open('./data/player_profiles.json', 'r') as file: 
        player_profile_data = json.load(file)

    return player_profile_data

# overwrite player profile data
def overwrite_player_profiles_data(player_profile_data):
    with open('./data/player_profiles.json', 'w') as file:
        json.dump(player_profile_data, file, indent=len(player_profile_data))

# initialises the player profile data
def initialise_player_profile(p_id):
    player_profile_data = get_player_profiles_data()

    if (f'{ p_id }' not in player_profile_data):
        player_profile_data[f'{ p_id }']={}
        player_profile_data[f'{ p_id }']['wins']=0
        player_profile_data[f'{ p_id }']['losses']=0

    overwrite_player_profiles_data(player_profile_data)

# gets currently running games data
def get_current_games():
    with open('./data/current_games.json', 'r') as file:
        current_games_data = json.load(file)

    return current_games_data

# overwrites currently running games data
def overwrite_current_games(current_games_data):
    with open('./data/current_games.json', 'w') as file:
        json.dump(current_games_data, file, indent=len(current_games_data))

# checks if the current user has already started a game
def is_in_game(p_id):
    current_games = get_current_games()

    is_gaming = False

    for game in current_games:
        if (game.find(f'{ p_id }') != -1):
            is_gaming = True
            break

    return is_gaming

# checks if the current user's game has already started
def is_game_ready(p_id):
    current_games = get_current_games()

    is_ready = False

    for game in current_games:
        if (game.find(f'{ p_id }') != -1):
            is_ready = current_games[game]['ready?']
            break

    return is_ready

# adds an accepted match to the current_games file, and returns the id of who was accepted
def add_to_current_games(p_id):
    current_games_data = get_current_games()
    queue_data = get_queue_data()
    dp = queue_data[f'{ p_id }']['dequeue_pointer']
    p2_id = queue_data[f'{ p_id }']['queue'][dp % 5]

    turn = random.randrange(0,2)
    if (turn == 0):
        turn = p_id
    else:
        turn = p2_id

    current_games_data[f'{ p_id }, { p2_id }']={}
    current_games_data[f'{ p_id }, { p2_id }']['turn']=turn
    current_games_data[f'{ p_id }, { p2_id }']['ready?']=False
    current_games_data[f'{ p_id }, { p2_id }'][f'{ p_id }']=None
    current_games_data[f'{ p_id }, { p2_id }'][f'{ p2_id }']=None
    current_games_data[f'{ p_id }, { p2_id }']['board']=['🟦', '🟦', '🟦', 
                                                         '🟦', '🟦', '🟦', 
                                                         '🟦', '🟦', '🟦']

    overwrite_current_games(current_games_data)
    delete_from_queue(p_id)
    return p2_id

# gets the game given a user
def get_player_game_stats(p_id):
    current_games_data = get_current_games()

    user_game = None

    for game in current_games_data:
        if (game.find(f'{ p_id }') != -1):
            user_game = current_games_data[game]
            break

    return user_game

# get player game
def get_player_game(p_id):
    current_games_data = get_current_games()

    user_game = None

    for game in current_games_data:
        if (game.find(f'{ p_id }') != -1):
            user_game = game
            break

    return user_game

# checks whether or not a player has already set an emoji for the game
def is_set_emoji(p_id):
    user_game = get_player_game_stats(p_id)

    return user_game[f'{ p_id }'] != None


# sets the in game emoji for a player
def set_emoji(p_id, reaction):
    current_games_data = get_current_games()
    player_game = get_player_game(p_id)
    opponent_id = get_opponent(p_id)

    current_games_data[player_game][f'{ p_id }'] = reaction
    current_games_data[player_game]['ready?'] = current_games_data[player_game][f'{ p_id }'] != None and current_games_data[player_game][f'{ opponent_id }'] != None

    overwrite_current_games(current_games_data)

# gets the emoji set by a user
def get_emoji(p_id):
    player_game_stats = get_player_game_stats(p_id)
    
    return player_game_stats[f'{ p_id }']

# gets the name of the opponent
def get_opponent(p_id):
    player_game = get_player_game(p_id)

    if (player_game.find(f'{ p_id }') == 0):
        return int(player_game[player_game.find(',') + 1:len(player_game)])
    else:
        return int(player_game[0:player_game.find(',')])

# adds a player vs bot game into the current games list
def add_bot_to_current_game(p_id, bot_id):
    current_games_data = get_current_games()

    turn = random.randrange(0, 2)
    if (turn == 0):
        turn = p_id
    else:
        turn = bot_id

    current_games_data[f'{ p_id }, { bot_id }']={}
    current_games_data[f'{ p_id }, { bot_id }']['turn']=turn
    current_games_data[f'{ p_id }, { bot_id }']['ready?']=False
    current_games_data[f'{ p_id }, { bot_id }'][f'{ p_id }']=None
    current_games_data[f'{ p_id }, { bot_id }'][f'{ bot_id }']='🤖'
    current_games_data[f'{ p_id }, { bot_id }']['board']=['🟦', '🟦', '🟦', 
                                                          '🟦', '🟦', '🟦', 
                                                          '🟦', '🟦', '🟦']

    overwrite_current_games(current_games_data)