from statbot.utils import total_time_to_hours_minutes
from statbot.classes import VoiceSession
from db.statistics import get_total_time_ranking_by_guild


def process_voice_sessions_for_statistics(guild_id):
    raw_voice_sessions = get_total_time_ranking_by_guild(guild_id)

    voice_session_list = []
    for session in raw_voice_sessions:
        user_id, total_time = session
        voice_session = VoiceSession(user_id=user_id, total_time=total_time_to_hours_minutes(total_time))
        voice_session_list.append(voice_session)
    return voice_session_list
