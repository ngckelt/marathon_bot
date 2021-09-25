from re import findall


def only_cyrillic(string: str) -> bool:
    cyrillic_count = findall(string=string, pattern="[а-яА-Я]")
    return len(cyrillic_count) == len(string)


def correct_msk_timedelta(msk_timedelta: str) -> bool:
    try:
        msk_timedelta = int(msk_timedelta)
        if msk_timedelta in range(-24, 24):
            return True
        return False
    except:
        return False

