# imports
import dotenv 

import os

from discord import Status
from discord.activity import Activity
from discord.enums import ActivityType
from discord import Intents
from discord.ext import commands
from discord import Embed
from discord import Colour 


# takes environment variables from .env file
dotenv.load_dotenv()

# storing the API key of the bot
ttt_token = os.getenv('API_KEY')

# allows bot to subscribe to all buckets of events 
intents = Intents.all()

# establishing the prefix to the bot
ttt = commands.Bot(command_prefix='>', intents=intents)

# loading on_join cog
ttt.load_extension('tictactoe_cogs.on_join.on_join')

# loading set_ttt_channel cog
ttt.load_extension('tictactoe_cogs.set_ttt_channel.set_ttt_channel')

# to ensure that the bot is running
@ttt.event
async def on_ready():
    print('ttt bot is ready')

# sends embedded message introducing the bot's self to the requesting user
@ttt.command(aliases=['TTT'])
async def TicTacToe(context):

    # sets up the status of the bot
    await ttt.change_presence(activity=Activity(type=ActivityType.playing, name=f'with {len(ttt.users)} gaming gamers!'), status=Status.onlilne, afk=False)

    ttt_greet=Embed(
        title=(':x: Hello, there! I\'m Tic Tac Toe Bot! :o:'),
        description=('''You\'ve probably guessed it! I\'m here to provide your server with the 
                        ability to play tic tac toe with your friends. If you\'re looking for a 
                        challenge, don\'t look any further! I\m right in fron of you!''' ), 
        colour=Colour.from_rgb(246,154,7)
    )
    ttt_greet.set_thumbnail(url=ttt.user.avatar_url)

    # sends the message to channel where the command was called
    await context.send(embed=ttt_greet)

#runs the bot
ttt.run(ttt_token)