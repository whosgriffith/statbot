from db.database_utils import db_connect_and_cursor
from loguru import logger


def get_user_ranking_by_guild(guild_id, afk_channel):
    try:
        con, cur = db_connect_and_cursor()
        query = "SELECT user_id, SUM(total_time) " \
                "FROM user_voice_sessions " \
                "WHERE guild_id = (%s) AND left_at IS NOT NULL AND afk_channel = (%s) " \
                "GROUP BY user_id " \
                "ORDER BY SUM(total_time) DESC "
        cur.execute(query, (guild_id, afk_channel))
        result = cur.fetchall()
        con.commit()
        con.close()
        return result
    except Exception as Ex:
        logger.exception("An error occurred while getting guild voice sessions:")
        print(Ex)


def get_channel_usage_by_guild(guild_id):
    try:
        con, cur = db_connect_and_cursor()
        query = "SELECT channel_id, SUM(total_time) " \
                "FROM user_voice_sessions " \
                "WHERE guild_id = (%s) AND left_at IS NOT NULL " \
                "GROUP BY channel_id " \
                "ORDER BY SUM(total_time) DESC "
        cur.execute(query, (guild_id,))
        result = cur.fetchall()
        con.commit()
        con.close()
        return result
    except Exception as Ex:
        logger.exception("An error occurred while getting channels stats:")
        print(Ex)


def get_usage_by_user(user_id, guild_id):
    try:
        con, cur = db_connect_and_cursor()
        query = "SELECT channel_id, total_time, afk_channel " \
                "FROM user_voice_sessions " \
                "WHERE user_id = (%s) AND guild_id = (%s) AND left_at IS NOT NULL " \
                "ORDER BY channel_id DESC "
        cur.execute(query, (user_id, guild_id))
        result = cur.fetchall()
        con.commit()
        con.close()
        return result
    except Exception as Ex:
        logger.exception("An error occurred while getting user stats:")
        print(Ex)


def get_channel_usage_by_user(user_id, guild_id):
    try:
        con, cur = db_connect_and_cursor()
        query = "SELECT channel_id, sum(total_time) " \
                "FROM user_voice_sessions " \
                "WHERE user_id = (%s) AND guild_id = (%s) AND left_at IS NOT NULL " \
                "GROUP BY channel_id " \
                "ORDER BY sum(total_time) DESC LIMIT 1 "
        cur.execute(query, (user_id, guild_id))
        result = cur.fetchall()
        con.commit()
        con.close()
        return result
    except Exception as Ex:
        logger.exception("An error occurred while getting user stats:")
        print(Ex)
