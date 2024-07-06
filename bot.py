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

# 加入語音頻道傳送加入訊息
#語音房進出訊息
@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:  # 加入語音頻道
        timestamp = int(datetime.datetime.now().timestamp())
        channel = after.channel
        voice_channel_id = after.channel.id
        embed = discord.Embed(title="", description="", color=0x26FF2A)
        embed.add_field(name='> :inbox_tray: 加入了語音頻道', value=f'時間：<t:{timestamp}>（<t:{timestamp}:R>）\n用戶：{member.mention}`（{member.name}）` \n頻道：{after.channel.mention}`（ID:{voice_channel_id}）`')
        await channel.send(embed=embed)
    elif before.channel is not None and after.channel is None:  # 離開語音頻道
        timestamp = int(datetime.datetime.now().timestamp())
        channel = before.channel
        voice_channel_id = before.channel.id
        embed = discord.Embed(title="", description="", color=0xFF0404)
        embed.add_field(name='> :outbox_tray: 離開了語音頻道', value=f'時間：<t:{timestamp}>（<t:{timestamp}:R>）\n用戶：{member.mention}`（{member.name}）` \n頻道：{before.channel.mention}`（ID:{voice_channel_id}）`')
        await channel.send(embed=embed)
    elif before.channel is not None and after.channel is not None and before.channel != after.channel:  # 切換語音頻道
        timestamp = int(datetime.datetime.now().timestamp())
        before_channel = before.channel
        after_channel = after.channel
        after_voice_channel_id = after.channel.id
        before_voice_channel_id = before.channel.id
        embed = discord.Embed(title="", description="", color=0x00bbff)
        embed.add_field(name='> :outbox_tray: 切換了語音頻道', value=f'時間：<t:{timestamp}>（<t:{timestamp}:R>）\n用戶：{member.mention}`（{member.name}）` \n頻道：{before.channel.mention}`（ID:{before_voice_channel_id}）` \n已到：{after.channel.mention}`（ID:{after_voice_channel_id}）`')
        await before_channel.send(embed=embed)
        embed = discord.Embed(title="", description="", color=0x00bbff)
        embed.add_field(name='> :inbox_tray: 切換了語音頻道', value=f'時間：<t:{timestamp}>（<t:{timestamp}:R>）\n用戶：{member.mention}`（{member.name}）` \n頻道：{after.channel.mention}`（ID:{after_voice_channel_id}）` \n已從：{before.channel.mention}`（ID:{before_voice_channel_id}）`')
        await after_channel.send(embed=embed)
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
        "傻眼": "傻甚麼眼?????",
        "唉"  : "怎麼了 ",
        "我好孤單"  : "沒關係你還有我 "
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
