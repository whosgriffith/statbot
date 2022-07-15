from loguru import logger
from statbot.voice_session import VoiceSession
from db.database_utils import db_connect_and_cursor


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
