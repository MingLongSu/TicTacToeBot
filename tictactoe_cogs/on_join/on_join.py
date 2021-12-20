from discord.ext import commands
from discord import Embed
from discord import Colour

from tictactoe_cogs.on_join.on_join_helpers import add_guild

class On_Join(commands.Cog):

    # new reference for ttt
    def __init__(self, ttt):
        self.ttt = ttt

    # to tell if the cog is ready
    @commands.Cog.listener()
    async def on_ready(self):
        print('on_join is ready!')

    # introductory message when the bot first joins the server
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        ttt_join_msg=Embed(
            title=(':x: Hi there, everyone! I\'m the one, the only, Tic Tac Toe Bot! :o:'),
            description=('''I\'m excited to provide you guys with a classic gaming experience and hope to face you all at least once!'''),
            colour=Colour.from_rgb(246,154,7)
        )
        ttt_join_msg.set_thumbnail(url=self.ttt.user.avatar_url)
        ttt_join_msg.set_footer(
            text=('PS. Owner! Remember to use \'>set_ttt_channel\' to set up a dedicated Tic Tac Toe channel!'),
            icon_url=self.ttt.user.avatar_url
        )

        # getting basic data on the server 
        add_guild(guild.id, guild.owner.id)

        # finds an available channel to introduce itself into
        for channel in guild.text_channels:
            if channel.name == 'general':
                await channel.send(embed=ttt_join_msg)
                break
            

# sets up the On_Join cog for ttt
def setup(ttt):
    ttt.add_cog(On_Join(ttt))
