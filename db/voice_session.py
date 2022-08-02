from datetime import datetime, timezone
from statbot.classes import VoiceSession
from db.database_utils import db_connect_and_cursor
from loguru import logger


def get_active_voice_session_by_user(user_id):
    voice_session = None
    try:
        con, cur = db_connect_and_cursor()
        query = "SELECT * FROM user_voice_sessions WHERE user_id=%s AND left_at IS null ORDER BY joined_at DESC LIMIT 1"
        cur.execute(query, (user_id, ))
        result = cur.fetchone()
        con.commit()
        con.close()
        if result:
            voice_session = VoiceSession(result[0], result[1], result[2], result[3], result[4], result[5], result[6])
        return voice_session
    except Exception as ex:
        logger.exception("An error occurred while getting active session from DB:")
        print(ex)


def save_join_datetime(member, channel):
    active_voice_session = get_active_voice_session_by_user(member.id)
    is_afk = member.guild.afk_channel == channel

    if not active_voice_session:
        try:
            con, cur = db_connect_and_cursor()
            query = "INSERT INTO user_voice_sessions (user_id, guild_id, channel_id, joined_at, afk_channel) " \
                    "VALUES (%s, %s, %s, %s, %s)"
            joined_at = datetime.now(timezone.utc)
            cur.execute(query, (member.id, member.guild.id, channel.id, joined_at, is_afk))
            con.commit()
            logger.info(f"Join datetime of {member.id} in voice channel {channel.id} saved")
            con.close()
        except Exception as ex:
            logger.error("An error occurred while saving joined_at datetime in DB:")
            print(ex)
    else:
        logger.warning(f"Active session for {member.id} in {channel.id} exists")


def save_leave_datetime(member, channel):
    try:
        active_session = get_active_voice_session_by_user(member.id)
        if active_session:
            con, cur = db_connect_and_cursor()
            query = "UPDATE user_voice_sessions SET left_at=(%s), total_time=(%s) WHERE session_id = (%s)"
            left_at = datetime.now(timezone.utc)
            timedelta_interval = (left_at - active_session.joined_at)
            cur.execute(query, (left_at, timedelta_interval, active_session.session_id))
            con.commit()
            logger.info(f"Leave datetime of user {member.id} in voice channel {channel.id} saved")
            con.close()
        else:
            logger.warning("No active session found")
    except Exception as ex:
        logger.exception("An error occurred while saving left_at datetime in DB:")
        print(ex)
