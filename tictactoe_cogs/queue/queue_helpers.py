import json

# gets the ttt channel
def get_ttt_channel(guild_id):
    with open('./data/all_guilds.json', 'r') as file:
        all_guild_data=json.load(file)

    return all_guild_data[f'{ guild_id }']['ttt_channel'] or None

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

# checks if queue is empty
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
    queue_data = get_queue_data(p_id)

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
            curr_queued_payer_wins = player_profile_data[f'{ p_id }']['wins']
            curr_queue_player_losses = player_profile_data[f'{ p_id }']['losses']
            display_queue.append([curr_queued_player_id, curr_queued_payer_wins, curr_queue_player_losses])
        else:
            display_queue.append([queue[start % 5], 'N/A', 'N/A'])

        if (start == end):
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

