class VoiceSession:
    def __init__(self, session_id, user_id, guild_id, channel_id, joined_at, left_at, total_time):
        self.session_id = session_id
        self.user_id = user_id
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.joined_at = joined_at
        self.left_at = left_at
        self.total_time = total_time
