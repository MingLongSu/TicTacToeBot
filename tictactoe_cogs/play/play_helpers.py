import json

from tictactoe_cogs.queue.queue_helpers import get_current_games, get_emoji, get_opponent, get_player_game, get_player_game_stats, overwrite_current_games

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