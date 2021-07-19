import re


cyrillic_symbols = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'j', 'з': 'z', 'й': 'j',
    'и': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
    'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'cc', 'ч': 'ch', 'ш': 'ha', 'щ': 'cha', 'ъ': '', 'ы': '', 'ь': '',
    'э': 'e', 'ю': 'u', 'я': 'ja', 'і': 'i', 'ї': 'ii', 'є': 'e'
}


def convert_cyrillic_to_ascii(raw_string):

    if raw_string.isascii():
        return raw_string
    else:
        return ''.join([cyrillic_symbols[i] if i in cyrillic_symbols else i for i in raw_string])


def slugify(s):
    pattern = r'[\W_]'
    return re.sub(pattern, '-', s).lower()


def time_delta(data, str_data=False):
    time_data = {}
    days = data.days
    seconds = data.seconds
    negative = True if days < 0 or seconds < 0 else False
    days = days * -1 if negative else days
    seconds = seconds * -1 if negative else seconds
    if data.days:
        if days > 30:
            time_data.update({'months': days // 30})
        if days % 30 >= 7:
            time_data.update({'weeks': days % 30 // 7})
        if days % 30 % 7 > 0:
            time_data.update({'days': days % 7})
        else:
            time_data.update({'days': days})
    if data.seconds:
        if seconds // 3600 >= 0:
            time_data.update({'hours': seconds // 3600})
        if seconds % 3600 > 0 and seconds // 60 > 0:
            time_data.update({'minutes': seconds % 3600 // 60})
    if negative:
        time_data = {k: v * -1 for k, v in time_data.items()}
    if str_data:
        return ', '.join([f'{v} {k}' for k, v in time_data.items()]) if time_data else '0 days'
    return time_data


