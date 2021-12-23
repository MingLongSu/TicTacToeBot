import asyncio

from discord.ext import commands
from discord import Embed
from discord import Colour

from tictactoe_cogs.play.play_helpers import add_play, correct_reaction, get_board, get_empty_positions, get_turn, is_tie, is_winner, set_next_turn
from tictactoe_cogs.queue.queue_helpers import get_opponent, get_ttt_channel, is_game_ready

class Play(commands.Cog):
    def __init__(self, ttt):
        self.ttt = ttt

    @commands.command(aliases=['grid', 'board', 'ttt'])
    async def play(self, context):
        ttt_channel = self.ttt.get_channel(get_ttt_channel(context.guild.id))

        # check if the game of the user is ready
        is_ready = is_game_ready(context.author.id)

        if (is_ready):
            # getting opponent of the player
            opponent = self.ttt.get_user(get_opponent(context.author.id))

            # getting the current turn
            turn = get_turn(context.author.id)

            # getting the board
            board = get_board(context.author.id)

            # getting the board positions that can still be played
            board_positions = get_empty_positions(context.author.id)

            match_msg=Embed(
                title=(f':x: { context.author.name } vs { opponent.name } :o:'),
                description=(f'Current player\'s turn: { self.ttt.get_user(turn).mention } '),
                colour = Colour.from_rgb(246,154,7)
            )
            match_msg.set_thumbnail(url=self.ttt.get_user(turn).avatar_url)
            sent_match_msg = await ttt_channel.send(embed=match_msg)
            sent_board_msg = await ttt_channel.send(board)

            # adding the reactions to the send_board_msg
            for board_position in board_positions:
                await sent_board_msg.add_reaction(board_position)

            try:
                # awaiting for the correct user to react to the message with the correct emoji
                reaction, user = await self.ttt.wait_for('reaction_add', timeout=60, check = lambda reaction, user : correct_reaction(board_positions, reaction) and user.id == turn)

                # getting new opponent based on the player of the current turn
                new_opponent = self.ttt.get_user(get_opponent(user.id))

                # set the turn of the next player
                set_next_turn(user.id)

                # add the new position to the player board
                add_play(user.id, reaction)

                # removes the reactions available after play is made
                await sent_board_msg.clear_reactions()

                # checks for a winner
                exists_winner_1 = is_winner(user.id)
                exists_winner_2 = is_winner(new_opponent.id)

                # checks for tie (PS. right now will be very poorly designed)
                is_tied = is_tie(user.id)

                if (exists_winner_1 != None): # if first player is winner
                    win_msg_1=Embed(
                        title=(f':partying_face: { user.name } has won against { new_opponent.name }!'),
                        description=(f':sparkles: Congratulations to both { user.mention } and { new_opponent.mention }, you both played exceptionally!'),
                        colour = Colour.from_rgb(246,154,7)
                    )
                    win_msg_1.set_thumbnail(url=user.avatar_url)
                    win_msg_1.set_footer(text='Use \'>request @player_name\' to request games against others!', icon_url=self.ttt.user.avatar_url)
                    await ttt_channel.send(embed=win_msg_1)
                elif (exists_winner_2 != None): # if second player is winner
                    win_msg_2=Embed(
                        title=(f':partying_face: { new_opponent.name } has won against { user.name }!'),
                        description=(f':sparkles: Congratulations to both { new_opponent.mention } and { user.mention }, you both played exceptionally!'),
                        colour = Colour.from_rgb(246,154,7)
                    )
                    win_msg_2.set_thumbnail(url=user.avatar_url)
                    win_msg_2.set_footer(text='Use \'>request @player_name\' to request games against others!', icon_url=self.ttt.user.avatar_url)
                    await ttt_channel.send(embed=win_msg_2)
                elif (is_tied): # if there is a tie
                    tie_msg=Embed(
                        title=(f':g::g: { user.name } has tied against { new_opponent.name }'), 
                        description=(f':sparkles: Well played by the both of you, { user.mention } and { new_opponent.mention }!'), 
                        colour = Colour.from_rgb(246,154,7)
                    )
                    tie_msg.set_thumbnail(url=self.ttt.user.avatar_url)
                    tie_msg.set_footer(text='Use \'>request @player_name\' to request games against others!', icon_url=self.ttt.user.avatar_url)
                    await ttt_channel.send(embed=tie_msg)

                # updates the board so that user is given confirmation of play going through
                await sent_board_msg.edit(content=get_board(user.id))
            except asyncio.TimeoutError: # when the player of the current turn has yet to respond
                timeout_msg=Embed(
                    title=(':no_entry_sign: Oh, an error occurred!'),
                    description=(f'Nothing to be concerned about though! It just seems that { self.ttt.get_user(turn).mention } has yet to make a play!'),
                    colour=Colour.from_rgb(246,154,7)
                )
                timeout_msg.set_footer(text='Use \'>play\' if you would like to make a play!', icon_url=self.ttt.user.avatar_url)
                timeout_msg.set_thumbnail(url=self.ttt.get_user(turn).avatar_url)
                await sent_match_msg.edit(embed=timeout_msg)
                await sent_board_msg.delete()
        else:
            wait_msg=Embed(
                title=(f':no_entry_sign: An Issue Occurred!'),
                description=(f'{ context.author.mention }, either you\'re not in a game or your opponent has not selected a piece yet!'),
                colour=Colour.from_rgb(246,154,7)
            )
            wait_msg.set_thumbnail(url=self.ttt.user.avatar_url)
            wait_msg.set_footer(text='Remember, use \'>set_piece\' to set your TTT piece!', icon_url=self.ttt.user.avatar_url)
            await ttt_channel.send(embed=wait_msg)


def setup(ttt):
    ttt.add_cog(Play(ttt))
