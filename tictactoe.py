# imports
from discord.ext.commands.core import command
import dotenv 

import os

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

# sends embedded message introducing the bot's self to the requesting user
@ttt.command(aliases=['TTT'])
async def TicTacToe(context):
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