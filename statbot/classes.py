class VoiceSession:
    def __init__(self, session_id=None, user_id=None, guild_id=None, channel_id=None, joined_at=None, left_at=None,
                 total_time=None, afk_channel=None):
        self.session_id = session_id
        self.user_id = user_id
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.joined_at = joined_at
        self.left_at = left_at
        self.total_time = total_time
        self.afk_channel = afk_channel
