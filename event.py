import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
from os.path import exists

# 確保 setting.json 存在
if not exists("setting.json"):
    raise FileNotFoundError("不要忘記放 setting.json 或者 cd 到指定資料夾去運行 py 哦~")

with open("setting.json", mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

class Event(Cog_Extension):

# 群主進入退出訊息
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(int(jdata['welcome_channel']))
        if channel:
            await channel.send(f'{member} 歡迎')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(int(jdata['Leave_channel']))
        if channel:
            await channel.send(f'{member} 有緣再相會')


    @commands.Cog.listener()   
    async def on_message(self, msg):
        if msg.content == 'apple':
            await msg.channel.send('hi')

def setup(bot): 
    bot.add_cog(Event(bot))        
