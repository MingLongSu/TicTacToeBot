from tictactoe_cogs.queue.queue_helpers import get_current_games, get_emoji, get_opponent, get_player_game, get_player_game_stats, get_player_profiles_data, overwrite_current_games, overwrite_player_profiles_data

# gets the game grid for a particular match
def get_board(p_id):
    max_length_row = 3 

    player_game_stats = get_player_game_stats(p_id)

    board = player_game_stats['board']

    display_board=''

    for i in range(len(board)):
        if (i % max_length_row == 0):
            display_board+='\n' + board[i]
        else:
            display_board+=board[i]

    return display_board

# gets the turn of the player
def get_turn(p_id):
    player_game_stats = get_player_game_stats(p_id)

    return player_game_stats['turn']

# finds all the board positions that have yet to be filled
def get_empty_positions(p_id):
    #dict of reaction emojis to place pieces on a board
    reactionable_emojis = {
        '1': '1\ufe0f\u20e3',
        '2': '2\ufe0f\u20e3', 
        '3': '3\ufe0f\u20e3',
        '4': '4\ufe0f\u20e3',
        '5': '5\ufe0f\u20e3',
        '6': '6\ufe0f\u20e3',
        '7': '7\ufe0f\u20e3',
        '8': '8\ufe0f\u20e3',
        '9': '9\ufe0f\u20e3',
    }

    player_game_stats = get_player_game_stats(p_id)

    board = player_game_stats['board']

    empty_positions = []

    for i in range(len(board)):
        if (board[i] == '🟦'):
            empty_positions.append(reactionable_emojis[f'{ i + 1 }'])
        
    return empty_positions

# checks if the player made a legal move on the board
def correct_reaction(board_positions, reaction):
    is_correct_reaction = False

    for i in range(len(board_positions)):
        if (str(reaction) == str(board_positions[i])):
            is_correct_reaction = True
            break
    
    return is_correct_reaction

# sets the turn to the next player
def set_next_turn(p_id):
    current_games_data = get_current_games()
    player_game = get_player_game(p_id)
    opponent = get_opponent(p_id)

    current_games_data[player_game]['turn'] = opponent

    overwrite_current_games(current_games_data)

# adds the play to the match board
def add_play(p_id, reaction):
    current_games_data = get_current_games()
    player_game = get_player_game(p_id)
    player_emoji = get_emoji(p_id)

    board = current_games_data[player_game]['board']

    index = int(str(reaction)[0:1]) - 1

    board[index] = str(player_emoji)

    current_games_data[player_game]['board'] = board

    overwrite_current_games(current_games_data)

# checks for a winner
def is_winner(p_id):
    player_games_stats = get_player_game_stats(p_id)
    board = player_games_stats['board']
    p_piece = get_emoji(p_id)

    # rows
    if (str(board[0]) == str(board[1]) == str(board[2]) == str(p_piece)):
        return p_id
    elif (str(board[3]) == str(board[4]) == str(board[5]) == str(p_piece)):
        return p_id
    elif (str(board[6]) == str(board[7]) == str(board[8]) == str(p_piece)): 
        return p_id
    # columns
    elif (str(board[0]) == str(board[3]) == str(board[6]) == str(p_piece)): 
        return p_id
    elif (str(board[1]) == str(board[4]) == str(board[7]) == str(p_piece)): 
        return p_id
    elif (str(board[2]) == str(board[5]) == str(board[8]) == str(p_piece)): 
        return p_id
    # diagonals
    elif (str(board[6]) == str(board[7]) == str(board[8]) == str(p_piece)): 
        return p_id
    elif (str(board[6]) == str(board[7]) == str(board[8]) == str(p_piece)): 
        return p_id
    else:
        return None

# checks for a tie
def is_tie(p_id):
    player_game_stats = get_player_game_stats(p_id)
    board = player_game_stats['board']

    is_tied = True

    for i in range(len(board)):
        if (board[i] == '🟦'):
            is_tied = False 
            break

    return is_tied
        
# add wins to a player profile
def add_wins(p_id):
    player_profiles_data = get_player_profiles_data()

    player_profiles_data[f'{ p_id }']['wins'] += 1

    overwrite_player_profiles_data(player_profiles_data)

# add losses to a player profile
def add_losses(p_id):
    player_profiles_data = get_player_profiles_data()

    player_profiles_data[f'{ p_id }']['losses'] += 1

    overwrite_player_profiles_data(player_profiles_data)

# concludes the game between two players (removes game from current_games data)
def conclude_game(p_id):
    current_games = get_current_games()
    player_game = get_player_game(p_id)

    del current_games[player_game]

    overwrite_current_games(current_games)
