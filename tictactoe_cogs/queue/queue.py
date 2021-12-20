from discord.ext import commands
from discord import Embed
from discord import Member
from discord import Colour

from tictactoe_cogs.queue.queue_helpers import add_to_queue, delete_from_queue, get_ttt_channel, initialise_queue, is_queue_empty, is_queue_full, is_queue_spam

class Queue(commands.Cog):
    def __init__(self, ttt):
        self.ttt = ttt
        
    # to tell that the queue cog is ready
    @commands.Cog.listener()
    async def on_ready(self):
        print('queue is ready!')

    # throws a user into the queue of the requested user
    @commands.command(aliases=['request', 'ttt_rg'])
    async def ttt_request_game(self, context, member:Member):
        # fetching the ttt channel
        ttt_channel = self.ttt.get_channel(get_ttt_channel(context.guild.id))


        if (member.id == self.ttt.user.id): # playing against the bot
            print("Feature to implement for another day")

        elif (context.author.id != member.id and member.bot == False): # queueing with another player
            # establishing p1 and p2 for ease of memory
            p1 = context.author
            p2 = member

            # initialiasing the queue of the players to the json file
            initialise_queue(p1.id)
            initialise_queue(p2.id)

            # check if the queue of p2 is full 
            is_full = is_queue_full(p2.id)

            # check if p1 is "spamming" p2's queue
            is_spamming = is_queue_spam(p1.id, p2.id)

            # determines whether or not a player will be able to be added to queue
            if (not is_full and not is_spamming):
                add_to_queue(p1.id, p2.id)

                success_msg=Embed(
                    title=(f':white_check_mark: { p1.name }, you have been added to { p2.name }\'s queue!'),
                    description=(f'Please wait patiently while { p2.name } decides who to play against!'),
                    colour = Colour.from_rgb(246,154,7)
                )
                success_msg.set_thumbnail(url=self.ttt.user.avatar_url)
                success_msg.set_footer(text=f'Use \'>queue_of @{ p1.name }\' to check your own queue!', icon_url=self.ttt.user.avatar_url)
                await ttt_channel.send(embed=success_msg)
            elif (is_full): # when queue of other player is full
                failure_msg=Embed(
                    title=(f':no_entry_sign: Sorry, { p1.name }. It seems that { p2.name }\'s queue is full right now.'),
                    description=(f'Please wait patiently for { p2.name }\'s queue to clear out a bit!'),
                    colour = Colour.from_rgb(246,154,7)
                )
                failure_msg.set_thumbnail(url=self.ttt.user.avatar_url)
                failure_msg.set_footer(text='Use \'>queue_of @player_name\' to check another player\'s queue!', icon_url=self.ttt.user.avatar_url)
                await ttt_channel.send(embed=failure_msg)
            else: # when requesting player has already been added to the queue
                failure_msg=Embed(
                    title=(f':no_entry_sign: Sorry, { p1.name }. It seems that you have already been added to { p2.name }\'s queue.'),
                    description=(f'Please wait patiently for { p2.name } to decide who to play with!'),
                    colour = Colour.from_rgb(246,154,7)
                )
                failure_msg.set_thumbnail(url=self.ttt.user.avatar_url)
                failure_msg.set_footer(text='Use \'>queue_of @player_name\' to check another player\'s queue!', icon_url=self.ttt.user.avatar_url)
                await ttt_channel.send(embed=failure_msg)
        else: # user queued against either another bot in the server or themself
            err_msg=Embed(
                title=(':no_entry_sign: Request couldn\'t be made!'),
                description=('This error message is to inform you that you either tried to play against yourself or another bot in ther server!'),
                colour=Colour.from_rgb(246,154,7)
            )
            err_msg.set_thumbnail(url=self.ttt.user.avatar_url)

            await ttt_channel.send(embed=err_msg)

    # removes the first player in the queue of a player
    @commands.command(aliases=['remove', 'ttt_r', 'skip'])
    async def ttt_skip_curr_player(self, context):
        ttt_channel = get_ttt_channel(context.guild.id)

        p = context.author

        # checking if the queue is empty
        is_empty = is_queue_empty(p.id)

        if (not is_empty):
            delete_from_queue(p.id)

            success_msg=Embed(
                title=(f':white_check_mark: Successfully removed a request from your queue, { p.name }!'),
                description=(''),
                colour = Colour.from_rgb(246,154,7)
            )
            success_msg.set_thumbnail(url=self.ttt.user.avatar_url)
            success_msg.set_footer(text=f'Use \'>queue_of @{ p.name }\' to check your own queue!', icon_url=self.ttt.user.avatar_url)
            await ttt_channel.send(embed=success_msg)
        else:
            null_remove_msg=Embed(
                title=(f':white_check_mark: Successfully removed... nothing from your queue, { p.name }!'),
                description=('Turns out your queue is actually empty!'),
                colour = Colour.from_rgb(246,154,7)
            )
            null_remove_msg.set_thumbnail(url=self.ttt.user.avatar_url)
            null_remove_msg.set_footer(text=f'Use \'>queue_of @{ p.name }\' to check your own queue!', icon_url=self.ttt.user.avatar_url)
            await ttt_channel.send(embed=null_remove_msg)

def setup(ttt):
    ttt.add_cog(Queue(ttt))
