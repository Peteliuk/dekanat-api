from datetime import datetime
from datetime import timedelta


def get_time(time_str):
    """
    :param time_str:        (string) time like `20:02`
    :return:                (object) converted string time to object time.struct_time
    """
    return datetime.strptime(time_str, '%H:%M')


def get_generated_subject_num(current_time):
    """
    Generates subject number by current time

    :param current_time:    (string) current time like `20:02`
    :return:                (int) generated subject number or None object
    """
    from project.models.functions import get_time_bounds
    time_bounds = get_time_bounds()
    if not time_bounds:
        return None
    subject_time = get_time(current_time)
    delta = timedelta(minutes=20)
    for time_bound in time_bounds:
        start_time = get_time(time_bound.start) - delta
        end_time = get_time(time_bound.end)
        if start_time <= subject_time < end_time:
            return time_bound.num
