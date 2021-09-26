

def seconds_to_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))


def get_message_text_by_marathon_day(marathon_day):
    message_text = f"Ты молодец, задание засчитано, ты уже сделал {marathon_day}/60"
    if marathon_day == 1:
        message_text = "Поздравляю с первым подъемом"
    elif marathon_day == 7 or marathon_day == 30:
        message_text = "Поздравляю, ты ближе к цели"
    return message_text

