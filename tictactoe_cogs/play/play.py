from discord.ext import commands
from discord import Embed
from discord import Colour

from tictactoe_cogs.play.play_helpers import get_board, get_empty_positions, get_turn
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
            board_msg = get_board(context.author.id)

            # getting the board positions that can still be played
            board_positions = get_empty_positions(context.author.id)

            match_msg=Embed(
                title=(f'{ context.author.name } vs { opponent.name }'),
                description=(f'Current player\'s turn: { self.ttt.get_user(turn).mention } '),
                colour = Colour.from_rgb(246,154,7)
            )
            match_msg.set_thumbnail(url=self.ttt.user.avatar_url)
            sent_match_msg = await ttt_channel.send(embed=match_msg)
            sent_board_msg = await ttt_channel.send(board_msg)

            # adding the reactions to the send_board_msg
            for board_position in board_positions:
                await sent_board_msg.add_reaction(board_position)

            # need to implement responding to the reactions so that turns can be played !!!
        else:
            wait_msg=Embed(
                title=(f':no_entry_sign: An Issue Occurred!'),
                description=(f'{ context.author.mention }, please wait patiently for the game to start! Either you or your opponent has not chosen an in-game piece yet!'),
                colour=Colour.from_rgb(246,154,7)
            )
            wait_msg.set_thumbnail(url=self.ttt.user.avatar_url)
            wait_msg.set_footer(text='Remember, use \'>set_piece\' to set your TTT piece!', icon_url=self.ttt.user.avatar_url)
            await ttt_channel.send(embed=wait_msg)


def setup(ttt):
    ttt.add_cog(Play(ttt))
