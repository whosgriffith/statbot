# Statbot └[∵┌]
import os
import discord
from dotenv import load_dotenv
from db.save_voice_session import save_join_datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


def process_join_voice_channel(member, after):
    print(f"{member.display_name} join {after.channel}")
    save_join_datetime(member, after.channel)


def process_leave_voice_channel(member, before):
    print(f"{member.display_name} left {before.channel}")


@client.event
async def on_voice_state_update(member, before, after):
    if before:
        process_leave_voice_channel(member, before)
    if after:
        process_join_voice_channel(member, after)

client.run(TOKEN)
