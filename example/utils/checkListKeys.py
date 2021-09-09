def checkListKeys(dic, keys):
    for k in keys:
        if k not in dic.keys():
            return False
    return True