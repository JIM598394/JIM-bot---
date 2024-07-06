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

# 確保 setting.json 存在
if not exists("setting.json"):
    raise FileNotFoundError("不要忘記放 setting.json 或者 cd 到指定資料夾去運行 py 哦~")

with open("setting.json", mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

bot = commands.Bot(command_prefix='[', intents=intents)

# 上線狀態
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.playing, name="💤"))
    print("機器人啟動成功")

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

# 加載擴展
for filename in os.listdir('. /cmds'):
    if filename.endswith('.py'):
        bot.load_extension(f'cmds.{filename[:-3]}')

# 加入語音頻道傳送加入訊息
@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel != after.channel:  # 確保只有在成員真正加入或離開語音頻道時才執行
        text_channel = member.guild.get_channel(int(jdata['VC_channel']))
        if text_channel:
            if after.channel and not before.channel:  # 成員加入語音頻道
                embed = discord.Embed(title="", description="", color=0x26FF2A)
                embed.add_field(name=':inbox_tray: 加入了語音頻道', value=f'{member.mention} 加入了 {after.channel.mention}')
                await text_channel.send(embed=embed)
            elif before.channel and not after.channel:  # 成員離開語音頻道
                embed = discord.Embed(title="", description="", color=0xFF0404)
                embed.add_field(name=':outbox_tray: 離開了語音頻道', value=f'{member.mention} 離開了 {before.channel.mention}')
                await text_channel.send(embed=embed)

# 自動回復
@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return
    
    responses = {
        "延遲": "正在計算延遲!!",
        "hello": "hello!",
        "嗨": "嗨嗨",
        ".": "點什麼點",
        "早安": "早安呀",
        "午安": "午安呀",
        "晚安": "晚安~ 住好眠",
        "安安": "安安呀",
        "你是誰": "我是JIM做出來玩的機器人喔",
        "test": "測試啥？",
        "傻眼": "傻甚麼眼?????"
    }

    if message.content in responses:
        reply_message = responses[message.content]
        if message.content == "延遲":
            pingmsg = await message.reply(reply_message, mention_author=False)
            ping = bot.latency * 1000
            ping = round(ping)
            await asyncio.sleep(3)
            await pingmsg.edit(content=f"延遲: {ping} 毫秒")
        else:
            await message.reply(reply_message, mention_author=False)

# 啟動機器人
if __name__ == "__main__":
    bot.run(jdata['TOKEN'])
