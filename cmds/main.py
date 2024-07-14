import discord
from discord.ext import commands
from core.classes import cog_Extension
import json
import datetime

class Main(cog_Extension):
    # 查看機器人延遲
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{self.bot.latency*1000} (ms)')
    
    # 這個指令要在函式內部定義
    @commands.command()      
    async def test(self, ctx):
        await ctx.send('123456789')

def setup(bot):
    bot.add_cog(Main(bot))
