from datetime import datetime


def get_pseudo_id_code_number(pseudo_ids):
    """
    :param self:
    :param pseudo_ids:
    :return: pseudo_id prefix
             pseudo_id number
    """
    if len(pseudo_ids) == 0:
        return None, 0

    elif pseudo_ids[-1] and '-' in pseudo_ids[-1]:
        prefix, znumber_str = pseudo_ids[-1].split('-')
        return prefix, int(znumber_str)

    else:
        return None, -1


def get_pd_row_index(df, value, column_name):
    """
    Returns pandas row index (label) for a row with a specific value in a specific column
    :param df: pandas dataframe
    :param value: specific value
    :param column_name: specific column
    :return: row index (label)
    """
    index = df.index
    idx_matches = index[df[column_name] == value].tolist()
    if len(idx_matches) == 1:
        return idx_matches[0]

    return None


def date_validate(value):
    """
    Validates and reformats an input date string
    :param value: date string
    :return: formatted datestring, or False if not a valid date string
    """
    format1 = "%Y-%m-%d"
    format2 = "%y%m%d"
    format3 = "%Y%m%d"

    try:
        date_obj = datetime.strptime(value, format1)
        return date_obj.strftime(format1)
    except:
        pass

    try:
        date_obj = datetime.strptime(value, format2)
        return date_obj.strftime(format1)
    except:
        pass

    try:
        date_obj = datetime.strptime(value, format3)
        return date_obj.strftime(format1)
    except:
        pass

    return False


def zfill_int(number):
    """
    Creates a number string with at most 8 leading zeros.
    :param number: integer
    :return: number string with leading zeros
    """
    number_str = str(number)

    return number_str.zfill(8)


def clear_layout(layout):
    """
    Processes a qt layout to clear it
    :param layout: qt layout
    :return: nothing
    """
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()


def to_list(obj):
    """
    Checks if obj is a list and returns it. If not, returns an empty list.
    :param obj:
    :return:
    """
    if isinstance(obj, list):
        return obj
    else:
        return []
