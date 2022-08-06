from datetime import datetime
from dateutil import relativedelta


def total_time_to_hours_minutes(total_time):
    hours, remainder = divmod(total_time.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{}h {}m".format(int(hours), int(minutes))


def format_join_date_for_user_stats(join_date):
    time_passed = relativedelta.relativedelta(datetime.now(), join_date)

    return f"{join_date.date()} ({time_passed.years} years {time_passed.months} months {time_passed.days} days ago)"
