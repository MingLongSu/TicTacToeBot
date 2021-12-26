from discord.ext import commands

class AI(commands.Cog): 
    def __init__(self, ttt):
        self.ttt = ttt

    


def setup(ttt):
    ttt.add_cog(AI(ttt))