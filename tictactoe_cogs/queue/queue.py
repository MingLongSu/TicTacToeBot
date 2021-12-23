import asyncio

from discord.ext import commands
from discord import Embed
from discord import Member
from discord import Colour

from tictactoe_cogs.queue.queue_helpers import add_to_current_games, add_to_queue, delete_from_queue, get_ttt_channel, initialise_player_profile, initialise_queue, is_game_ready, is_in_game, is_queue_empty, is_queue_full, is_queue_spam, is_set_emoji, make_queue_display, set_emoji

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

            # initialising the player profile of both players
            initialise_player_profile(p1.id)
            initialise_player_profile(p2.id)

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
        ttt_channel = self.ttt.get_channel(get_ttt_channel(context.guild.id))

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

    # allows use to view the queue of any player (including self), aside from bots
    @commands.command(aliases=['view_queue'])
    async def queue_of(self, context, member:Member):
        ttt_channel = self.ttt.get_channel(get_ttt_channel(context.guild.id))

        # initialising the queue of @'d member in case they never requested for a game
        initialise_queue(member.id)

        # initialising the player profile of the @'d member
        initialise_player_profile(member.id)

        if (member.bot):
            bot_msg=Embed(
                title=(':no_entry_sign: Hey! You just tried to view the queue of a bot!'),
                description=('If you didn\'t know, bots don\'t have a queue! Also, the only bot you can face is the master of tic tac toe being me.'),
                colour=Colour.from_rgb(246,154,7)
            )
            bot_msg.set_thumbnail(url=member.avatar_url)
            bot_msg.set_footer(text='Use \'>queue_of @player_name\' to check another player\'s queue!', icon_url=self.ttt.user.avatar_url)
            await ttt_channel.send(embed=bot_msg)
        else:
            player_queue_data = make_queue_display(member.id)

            player_queue_msg=Embed(
                title=(f':x: { member.name }\'s queue! :o:'),
                description=(''), 
                colour=Colour.from_rgb(246,154,7)
            )
            player_queue_msg.set_thumbnail(url=member.avatar_url)
            player_queue_msg.set_footer(text='Use \'>queue_of @player_name\' to check another player\'s queue!', icon_url=self.ttt.user.avatar_url)
            for i in range(len(player_queue_data)):
                player_queue_msg.add_field(
                    name=(f'{ i + 1 }. { self.ttt.get_user(player_queue_data[i][0]) }'),
                    value=(f'Wins: { player_queue_data[i][1] } Losses: { player_queue_data[i][2] }'),
                    inline=False
                )
            await ttt_channel.send(embed=player_queue_msg)     

    # accepting user requests
    @commands.command(aliases=['accept'])
    async def accept_curr_game(self, context):
        ttt_channel = self.ttt.get_channel(get_ttt_channel(context.guild.id))

        # initialising queues
        initialise_queue(context.author.id)

        # initialising player profiles
        initialise_player_profile(context.author.id)

        # checks if the queue is empty
        is_empty = is_queue_empty(context.author.id)

        # checks if the acceptor or player are already in a game
        is_gaming = is_in_game(context.author.id)

        if (not is_empty and not is_gaming):
            p2 = self.ttt.get_user(add_to_current_games(context.author.id))

            challenge_msg=Embed(
                title=(f'{ context.author.name } vs. { p2.name }!'),
                description=(f'{ context.author.mention } has accepted a game against { p2.mention }! May the greater player be victorious!'),
                colour=Colour.from_rgb(246,154,7)
            )
            challenge_msg.set_thumbnail(url=self.ttt.user.avatar_url)
            challenge_msg.set_footer(text='Use \'>set_piece\' to select your tic-tac-toe game pieces!')
            await ttt_channel.send(embed=challenge_msg)
        else:
            fail_msg=Embed(
                title=(f':no_entry_sign: Oh, { context.author.name }, an error occurred!'),
                description=('There is currently no one in your queue or your\'re currently in a match! Please finish your game first or request for a game against either other player or myself, the master of TTT!'),
                colour=Colour.from_rgb(246,154,7)
            )
            fail_msg.set_footer(text=f'Use \'>request @player_name\' to request a game with another player!', icon_url=self.ttt.user.avatar_url)
            fail_msg.set_thumbnail(url=self.ttt.user.avatar_url)
            await ttt_channel.send(embed=fail_msg)

    # sets a player's in-game piece indicator
    @commands.command(aliases=['s_emoji'])
    async def set_piece(self, context):
        ttt_channel = self.ttt.get_channel(get_ttt_channel(context.guild.id))

        # check if in game
        is_ready = is_game_ready(context.author.id)

        # check if emoji has already been set
        is_emojied = is_set_emoji(context.author.id)

        # checks whether emoji has been set and is gaming
        if (not is_emojied and not is_ready):
            react_msg = Embed(
                title=(f':wave: Hi there, { context.author.name }!'),
                description=(f'React to this message using an emoji in order to set your in game piece!'),
                colour = Colour.from_rgb(246,154,7)
            )
            react_msg.set_thumbnail(url=self.ttt.user.avatar_url)

            sent_react_msg = await ttt_channel.send(embed=react_msg)

            # waiting for player to set in game piece
            try:
                reaction, user = await self.ttt.wait_for('reaction_add', timeout=60, check=lambda reaction, user : user == context.author and str(reaction.emoji) != '🟦')

                # embed to signal the confirmation of a newly set game piece
                edited_react_msg=Embed(
                    title=(f':white_check_mark: { user.name }, you have set your game piece to { str(reaction.emoji) }!'),
                    description=('I wish you good luck with your game!'),
                    colour = Colour.from_rgb(246,154,7)
                )
                edited_react_msg.set_thumbnail(url=self.ttt.user.avatar_url)
                edited_react_msg.set_footer(text='Use \'>play\' to attempt to start the Tic-Tac_Toe game!', icon_url=self.ttt.user.avatar_url)

                await sent_react_msg.edit(embed=edited_react_msg)

                # setting emoji in the game_data
                set_emoji(context.author.id, str(reaction))
            except asyncio.TimeoutError:
                expired_msg = Embed(
                    title=(":no_entry_sign: Oh, your time has expired!"),
                    description=('Use \'>ttt_set_emoji\' again to set your emoji!'),
                    colour = Colour.from_rgb(246,154,7)
                )
                expired_msg.set_thumbnail(url=self.ttt.user.avatar_url)

                await ttt_channel.send(embed=expired_msg)
        else:
            error_message=Embed(
                title=(':no_entry_sign: Oh no, an error occurred!'),
                description=('One of following two issues might have happened:'),
                colour = Colour.from_rgb(246,154,7)
            )
            error_message.add_field(
                name=('Issue #1: Emoji already set!'),
                value=('Sorry, but setting emojis are one and done!'),
                inline=False
            )
            error_message.add_field(
                name=('Issue #2: Already in game!'),
                value=('Switching pieces mid game is kinda cheating!'),
                inline=False
            )
            error_message.set_thumbnail(url=self.ttt.user.avatar_url)
            await ttt_channel.send(embed=error_message)

def setup(ttt):
    ttt.add_cog(Queue(ttt))
