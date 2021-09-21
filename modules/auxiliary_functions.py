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


def zfill_int(number):
    number_str = str(number)

    return number_str.zfill(8)


def clear_layout(self, layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()


def to_list(obj):
    if type(obj) is list:
        return obj
    else:
        return []