import os
import discord
from dotenv import load_dotenv
from db.voice_session import save_join_datetime, save_leave_datetime
from db.database_utils import active_sessions_cleanup

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    active_sessions_cleanup()


@client.event
async def on_voice_state_update(member, before, after):

    channel_changed = before.channel != after.channel
    if channel_changed:
        if before.channel:
            save_leave_datetime(member, before.channel)
        if after.channel:
            save_join_datetime(member, after.channel)

client.run(TOKEN)
