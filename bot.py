# 機器人設定
import asyncio
import discord
from discord.ext import commands
import json
import os
import tracemalloc
from os.path import exists
import datetime


# 啟用 tracemalloc
tracemalloc.start()

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='e/',  intents=intents)
bot.remove_command('help')

# 確保 setting.json 存在
if not exists("setting.json"):
    raise FileNotFoundError("不要忘記放 setting.json 或者 cd 到指定資料夾去運行 py 哦~")

with open("setting.json", mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

# 上線狀態
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.playing, name=""))
    print(f'✅ {bot.user.name} 已經準備好了！')


# 群主進入退出訊息
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(int(jdata['welcome_channel']))
    if channel:
        await channel.send(f'{member.mention} 歡迎')

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(int(jdata['Leave_channel']))
    if channel:
        await channel.send(f'{member.mention} 有緣再相會')

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cmds.{extension}')
    await ctx.send(f'loaded{extension} done.')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extensionload_extension(f'cmds.{extension}')
    await ctx.send(f'UN-loaded{extension} done.')

@bot.command()
async def reload(ctx, extension):
    bot.reload_extensionload_extension(f'cmds.{extension}')
    await ctx.send(f'RE-loaded{extension} done.')                

# 加載擴展
for filename in os.listdir('./cmds'):
    if filename.endswith('. py'):
        bot.load_extension(f'cmds.{filename[:-3]}')


# 啟動機器人
if __name__ == "__main__":
    bot.run(jdata['TOKEN'])
