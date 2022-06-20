import psycopg2


def get_active_voice_session_by_user(username):
    try:
        con = psycopg2.connect(database="statbot", user="risker", password="root", host="localhost", port="5432")
        cur = con.cursor()
        query = "SELECT * FROM user_voice_sessions WHERE username=%s AND left_at=null ORDER BY joined_at DESC LIMIT 1"

        cur.execute(query, (username, ))
        result = cur.fetchone()
        con.commit()
        con.close()
        return result
    except Exception as ex:
        print("An error occurred while getting active session from DB:")
        print(ex)
