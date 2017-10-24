# coding=utf-8


def prints(*args, if_print=True):
    """
    determine if log info printed
    :param if_print: control switch
    :return:
    """
    if if_print:
        print(*args)