import os
import discord
from discord.ext import commands
from db.voice_session import save_join_datetime, save_leave_datetime
from db.database_utils import active_sessions_cleanup
from statbot.process_statistics import process_voice_sessions_for_statistics, \
    process_data_for_channel_statistics, process_data_for_user_statistics
from statbot.utils import total_time_to_hours_minutes
from loguru import logger

TOKEN = os.environ.get('DISCORD_TOKEN')

intents = discord.Intents(messages=True, guilds=True, members=True, voice_states=True)
bot = commands.Bot(command_prefix='.statbot ', intents=intents)
bot.remove_command("help")


@bot.event
async def on_ready():
    active_sessions_cleanup()
    activity = discord.Game(name=".statbot help")
    await bot.change_presence(activity=activity)


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
            user_ = bot.get_user(voice_session.user_id)
            content += f"**{index} - {user_.display_name}** ({voice_session.total_time})\n"
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
            user_ = bot.get_user(voice_session.user_id)
            content += f"**{index} - {user_.display_name}** ({voice_session.total_time})\n"
        except Exception as Ex:
            logger.exception("An error occurred while getting AFK time by user:")
            print(Ex)

    embed = discord.Embed(title=F"{ctx.guild.name} - AFK Time",
                          description=content,
                          color=744700)

    await ctx.send(embed=embed)


@bot.command()
async def channels(ctx):
    channels_data_list = process_data_for_channel_statistics(ctx.guild.id)
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


@bot.command()
async def user(ctx, member: discord.Member):
    try:
        usage_data = process_data_for_user_statistics(member)

        if usage_data.get('status') == 'no-data':
            content = usage_data['message']
        else:
            fav_channel_name = bot.get_channel(usage_data['most_used_channel']['id'])
            content = f"Total voice sessions: **{usage_data['total_voice_sessions']}**\n" \
                      f"Most used channel: **{fav_channel_name} ({usage_data['most_used_channel']['time']})**\n" \
                      f"Connected to voice channels: **{usage_data['on_voice_time']}**\n" \
                      f"AFK time: **{usage_data['afk_time']}**\n" \
                      f"Roles: **{usage_data['roles']}**\n" \
                      f"Joined guild: **{usage_data['join_date']}**"

        embed = discord.Embed(title=f"Statistics",
                              description=content,
                              color=744700)
        embed.set_author(name=member.display_name, icon_url=member.avatar_url)

        await ctx.send(embed=embed)

    except Exception as Ex:
        logger.exception("An error occurred while getting channel usage:")
        print(Ex)


@bot.command()
async def help(ctx):
    content = "**ranks** (Voice channels usage ranking by user)\n" \
              "**afk** (AFK channel usage by user)\n" \
              "**channels** (Voice channels usage time)\n" \
              "**user** @user (User stats)\n"
    embed = discord.Embed(title="Statbot Commands", description=content, color=744700)
    embed.set_footer(text="(Use .statbot <command>)")
    await ctx.author.send(embed=embed)
    await ctx.message.add_reaction("✅")

bot.run(TOKEN)
