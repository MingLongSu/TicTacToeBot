# produces the best possibly play given a board [board_data] and the players
from tictactoe_cogs.ai.ai_helpers import explore


def get_best_play(board_data, p_emoji, bot_emoji):
    print(board_data)
    best_play_value = -1000
    best_play = -1

    # exploring possible ways a game could played out considering the board state, and retains the best (so far)
    for i in range(len(board_data)):
        if (board_data[i] == '🟦'):
            board_data[i] = str(bot_emoji)

            curr_play_value = explore(board_data, 0, False, p_emoji, bot_emoji)

            board_data[i] = '🟦'

            if (curr_play_value > best_play_value):
                best_play_value = curr_play_value
                best_play = i

    return best_play
            