from datetime import datetime, timezone
import psycopg2
from db.get_active_voice_session import get_active_voice_session_by_user


def save_join_datetime(member, channel):
    username = member.display_name
    active_voice_session = get_active_voice_session_by_user(username)

    if active_voice_session:
        try:
            con = psycopg2.connect(database="statbot", user="risker", password="root", host="localhost", port="5432")
            cur = con.cursor()
            query = "INSERT INTO user_voice_sessions (username, channel, joined_at) " \
                    "VALUES (%s, %s, %s)"
            joined_at = datetime.now(timezone.utc)
            print(f"Joined_at: {joined_at}")
            print(f"Channel_name: {channel.name}")
            print(f"Channel_id: {channel.id}")
            cur.execute(query, (username, channel.name, joined_at))
            con.commit()

            print(f"Join datetime of {username} in voice channel \"{channel}\" saved successfully")
            con.close()
        except Exception as ex:
            print("An error occurred while saving join datetime in DB:")
            print(ex)


def save_leave_datetime(user, channel):
    try:
        # con = psycopg2.connect(database="statbot", user="risker", password="root", host="localhost", port="5432")
        # cur = con.cursor()
        # query = "INSERT INTO users_voice_stats (username, channel, joined_at, left_at, total_time) " \
        #         "VALUES (%s, %s, %s, %s, %s)"
        current_time = datetime.now()

        # cur.execute(query, (user, channel, joined_at, left_at, total_time))

        # con.commit()
        print(f"Leave datetime of {user} in voice channel \"{channel}\" saved successfully")
        # con.close()
    except Exception as ex:
        print("An error occurred while saving leave datetime in DB:")
        print(ex)
