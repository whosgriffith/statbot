def total_time_to_hours_minutes(total_time):
    hours, remainder = divmod(total_time.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{}h {}m".format(int(hours), int(minutes))
