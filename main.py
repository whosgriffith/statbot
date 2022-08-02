import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from db.voice_session import save_join_datetime, save_leave_datetime
from db.database_utils import active_sessions_cleanup
from statbot.process_statistics import process_voice_sessions_for_statistics, \
    process_voice_sessions_for_channel_statistics
from statbot.utils import total_time_to_hours_minutes
from loguru import logger


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents(messages=True, guilds=True, members=True, voice_states=True)
bot = commands.Bot(command_prefix='.statbot ', intents=intents)


@bot.event
async def on_ready():
    active_sessions_cleanup()


@bot.event
async def on_voice_state_update(member, before, after):
    channel_changed = before.channel != after.channel

    if channel_changed and not member.bot:
        if before.channel:
            save_leave_datetime(member, before.channel)
        if after.channel:
            save_join_datetime(member, after.channel)


@bot.command()
async def ranks(ctx):
    statistics_list = process_voice_sessions_for_statistics(ctx.guild.id)
    content = "Ranking calculated by the sum of time spent on all voice channels (Except AFK).\n \n"

    for index, voice_session in enumerate(statistics_list, 1):
        try:
            user = bot.get_user(voice_session.user_id)
            content += f"**{index} - {user.display_name}** ({voice_session.total_time})\n"
        except Exception as Ex:
            logger.exception("An error occurred while getting guild rank for voice sessions:")
            print(Ex)

    embed = discord.Embed(title=F"{ctx.guild.name} - Ranks",
                          description=content,
                          color=744700)

    await ctx.send(embed=embed)


@bot.command()
async def afk(ctx):
    afk_time_list = process_voice_sessions_for_statistics(ctx.guild.id, True)
    content = "Time on AFK channel by user.\n \n"

    for index, voice_session in enumerate(afk_time_list, 1):
        try:
            user = bot.get_user(voice_session.user_id)
            content += f"**{index} - {user.display_name}** ({voice_session.total_time})\n"
        except Exception as Ex:
            logger.exception("An error occurred while getting AFK time by user:")
            print(Ex)

    embed = discord.Embed(title=F"{ctx.guild.name} - AFK Time",
                          description=content,
                          color=744700)

    await ctx.send(embed=embed)


@bot.command()
async def channels(ctx):
    channels_data_list = process_voice_sessions_for_channel_statistics(ctx.guild.id)
    content = "Most used channels.\n \n"

    for index, channel_data in enumerate(channels_data_list, 1):
        try:
            channel = bot.get_channel(channel_data[0])
            channel_total_time = total_time_to_hours_minutes(channel_data[1])
            content += f"**{index} - {channel.name}** ({channel_total_time})\n"
        except Exception as Ex:
            logger.exception("An error occurred while getting channel usage:")
            print(Ex)

    embed = discord.Embed(title=f"{ctx.guild.name} - Channels usage",
                          description=content,
                          color=744700)

    await ctx.send(embed=embed)

bot.run(TOKEN)
