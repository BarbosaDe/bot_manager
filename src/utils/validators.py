def is_int(string):
    try:
        return abs(int(string))
    except ValueError:
        return


def is_float(string):
    try:
        return float(string)
    except ValueError:
        return
