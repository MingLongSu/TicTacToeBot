# produces a boolean value where true indicates no moves left on the board (tie), and false otherwise (not a tie)
#   given a board [board_data].
def is_tie(board_data): 
    for piece in board_data:
        if (piece == '🟦'):
            return False
    
    return True

# produces a score representing the result of the ai committing to a particular play
def win_conditions(board_data, p_emoji, bot_emoji):
    # checking for wins in terms of a row combo
    if (board_data[0] == board_data[1] == board_data[2]):
        if (board_data[0] == str(bot_emoji)):
            return 10
        elif (board_data[0] == str(p_emoji)):
            return -10
    elif (board_data[3] == board_data[4] == board_data[5]):
        if (board_data[3] == str(bot_emoji)):
            return 10
        elif (board_data[3] == str(p_emoji)):
            return -10
    elif (board_data[6] == board_data[7] == board_data[8]):
        if (board_data[6] == str(bot_emoji)):
            return 10
        elif (board_data[6] == str(p_emoji)):
            return -10
    
    # checking for wins in terms of a column combo
    if (board_data[0] == board_data[3] == board_data[6]):
        if (board_data[0] == str(bot_emoji)):
            return 10
        elif (board_data[0] == str(p_emoji)):
            return -10
    elif (board_data[1] == board_data[4] == board_data[7]):
        if (board_data[1] == str(bot_emoji)):
            return 10
        elif (board_data[1] == str(p_emoji)):
            return -10
    elif (board_data[2] == board_data[5] == board_data[8]):
        if (board_data[2] == str(bot_emoji)):
            return 10
        elif (board_data[2] == str(p_emoji)):
            return -10

    # checking for wins in terms of a diagonal combo
    if (board_data[0] == board_data[4] == board_data[8]):
        if (board_data[0] == str(bot_emoji)):
            return 10
        elif (board_data[0] == str(p_emoji)):
            return -10
    elif (board_data[2] == board_data[4] == board_data[6]):
        if (board_data[2] == str(bot_emoji)):
            return 10
        elif (board_data[2] == str(p_emoji)):
            return -10

    # otherwise 0 is returned to indicate that neither has one from this play
    return 0

# further explores combinations of plays to examine the results of each play
def explore(board_data, depth, is_maximiser_turn, p_emoji, bot_emoji):
    result = win_conditions(board_data, p_emoji, bot_emoji)

    # if the path of plays results in a win for the bot
    if (result == 10):
        return result
    
    # if the path of plays results in a win for the player
    if (result == -10):
        return result

    # if the path of plays results in a tie
    if (is_tie(board_data)):
        return 0

    if (is_maximiser_turn): # if it is the turn of the bot
        best_value = -1000

        for i in range(len(board_data)):
            if (board_data[i] == '🟦'):
                board_data[i] = bot_emoji

                best_value = max(best_value, explore(board_data, depth + 1, not is_maximiser_turn, p_emoji, bot_emoji))

                board_data[i] = '🟦'
        return best_value
    else: # if it is the turn of the player
        best_value = 1000

        for i in range(len(board_data)):
            if (board_data[i] == '🟦'):
                board_data[i] = p_emoji

                best_value = min(best_value, explore(board_data, depth + 1, not is_maximiser_turn, p_emoji, bot_emoji))

                board_data[i] = '🟦'
        return best_value

