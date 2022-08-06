from datetime import timedelta
from statbot.utils import total_time_to_hours_minutes, format_join_date_for_user_stats
from statbot.classes import VoiceSession
from db.statistics import get_user_ranking_by_guild, get_channel_usage_by_guild, get_usage_by_user, \
    get_channel_usage_by_user


def process_voice_sessions_for_statistics(guild_id, afk_channel=False):
    raw_voice_sessions = get_user_ranking_by_guild(guild_id, afk_channel)

    voice_session_list = []
    for session in raw_voice_sessions:
        user_id, total_time = session
        voice_session = VoiceSession(user_id=user_id, total_time=total_time_to_hours_minutes(total_time))
        voice_session_list.append(voice_session)
    return voice_session_list


def process_data_for_channel_statistics(guild_id):
    raw_channels_data_list = get_channel_usage_by_guild(guild_id)

    channels_data_list = []
    for channel_data in raw_channels_data_list:
        channels_data_list.append(channel_data)
    return channels_data_list


def process_data_for_user_statistics(user):
    usage_data_by_user = get_usage_by_user(user.id, user.guild.id)
    channels_usage = get_channel_usage_by_user(user.id, user.guild.id)

    if not channels_usage:
        return {'status': 'no-data', 'message': 'No data (• ิ _ • ิ)?'}

    on_voice_time_td = timedelta(0)
    afk_time_td = timedelta(0)
    for usage_data in usage_data_by_user:
        voice_session = VoiceSession(channel_id=usage_data[0], total_time=usage_data[1], afk_channel=usage_data[2])
        if voice_session.afk_channel is False:
            on_voice_time_td += voice_session.total_time
        else:
            afk_time_td += voice_session.total_time

    roles_list = []
    for role in user.roles:
        roles_list.append(role.name.replace('@', ''))

    result = {
        'total_voice_sessions': len(usage_data_by_user),
        'on_voice_time': total_time_to_hours_minutes(on_voice_time_td),
        'afk_time': total_time_to_hours_minutes(afk_time_td),
        'roles': ','.join(roles_list),
        'join_date': format_join_date_for_user_stats(user.joined_at),
        'most_used_channel': {'id': channels_usage[0][0], 'time': total_time_to_hours_minutes(channels_usage[0][1])}
    }

    return result
