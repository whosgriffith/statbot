import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from db.voice_session import save_join_datetime, save_leave_datetime
from db.database_utils import active_sessions_cleanup
from statbot.voice_session import process_voice_sessions_for_statistics

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
    if channel_changed:
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
            print(Ex)

    embed = discord.Embed(title=F"{ctx.guild.name} - Ranks",
                          description=content,
                          color=744700)

    await ctx.send(embed=embed)

bot.run(TOKEN)
