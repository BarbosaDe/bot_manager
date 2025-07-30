def type_check(string, type):
    try:
        return type(string)
    except ValueError:
        return
