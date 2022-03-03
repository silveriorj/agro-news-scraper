from datetime import datetime


def remove_breakline_from_dict(dictionary):
    for key in dictionary:
        dictionary[key] = dictionary[key].replace('\n', '').replace('  ', '')
    return dictionary


def format_date(date, date_format_from, date_format_to='%d/%m/%Y'):
    date = datetime.strptime(
        date.capitalize().strip(),
        date_format_from.strip()
    )
    return date.strftime(date_format_to)
