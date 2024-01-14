from typing import Literal
from datetime import datetime


def date_conversion(unix_date: int, output: Literal['date', 'time', 'datetime']) -> str:
    """
    Converts unix date format into time
    :param unix_date: the unix date to be converted
    :param output: the desired format
    :return: the formatted unix_date
    """
    date_time = datetime.fromtimestamp(unix_date)
    if output is 'date':
        return date_time.strftime("%Y-%m-%d")
    elif output is 'time':
        return date_time.strftime("%H:%M:%S")
    elif output is 'datetime':
        return date_time.strftime("%Y-%m-%d, %H:%M:%S" )


def resize_window(old_width, old_height, new_width, new_height):
    old_width = new_width
    old_height = new_height
