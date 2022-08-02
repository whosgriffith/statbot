from db.database_utils import db_connect_and_cursor
from loguru import logger


def get_total_time_ranking_by_guild(guild_id):
    try:
        con, cur = db_connect_and_cursor()
        query = "SELECT user_id, SUM(total_time) " \
                "FROM user_voice_sessions " \
                "WHERE guild_id = (%s) AND left_at IS NOT NULL " \
                "GROUP BY user_id " \
                "ORDER BY SUM(total_time) DESC "
        cur.execute(query, (guild_id, ))
        result = cur.fetchall()
        con.commit()
        logger.info(f"Selected {cur.rowcount} voice sessions in guild {guild_id}")
        con.close()
        return result
    except Exception as Ex:
        logger.exception("An error occurred while getting guild voice sessions:")
        print(Ex)
