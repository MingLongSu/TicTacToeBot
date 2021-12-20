import json

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
    queue_data = get_queue_data()

    dp = queue_data[f'{ p_id }']['dequeue_pointer']
    queue_data[f'{ p_id }']['queue'][dp % 5] = None
    queue_data[f'{ p_id }']['dequeue_pointer'] += 1

    overwrite_queue_data(queue_data)