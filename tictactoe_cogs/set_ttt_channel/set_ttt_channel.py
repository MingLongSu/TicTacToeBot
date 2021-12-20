from discord.ext import commands
from discord import Embed
from discord import Colour

from tictactoe_cogs.set_ttt_channel.set_ttt_channel_helpers import get_all_guilds, overwrite_all_guilds

class Set_TTT_Channel(commands.Cog):
    def __init__(self, ttt):
        self.ttt = ttt
        
    # to tell that the set_ttt_channel cog is ready
    @commands.Cog.listener()
    async def on_ready(self):
        print('set_ttt_channel is ready!')

    # sets the ttt channel for a particular server
    @commands.command(aliases=['Set_TTT_C', 'stttc', 'Set_TTT_Channel'])
    async def set_ttt_channel(self, context):
        context.message.delete
        all_guild_data=get_all_guilds()
        author=context.author.id
        current_guild=context.guild.id
        current_channel=context.channel.id

        # checks if user is the owner who requested a change
        if (author == all_guild_data[f'{ current_guild }']['owner_id']):
            # owner has made changes to the channel for TTT
            all_guild_data[f'{ current_guild }']['ttt_channel']=current_channel
            overwrite_all_guilds(all_guild_data)

            success_msg=Embed(
                title=(':white_check_mark: TicTacToe Channel Set!'),
                description=(''),
                colour=Colour.from_rgb(246,154,7)
            )

            await self.ttt.get_channel(current_channel).send(embed=success_msg)
        else:
            # not the owner who prompted change
            not_owner_msg=Embed(
                title=(':octagonal_sign: Hey, you aren\'t the owner!'),
                description=('If you think there should be changes to where the TTT channel should be, please contact your server owner!'),
                colour=Colour.from_rgb(246,154,7)
            )
            not_owner_msg.set_thumbnail(url=self.ttt.user.avatar_url)

            await context.send(embed=not_owner_msg)

def setup(ttt):
    ttt.add_cog(Set_TTT_Channel(ttt))
