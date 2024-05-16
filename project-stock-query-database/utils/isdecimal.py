from decimal import Decimal

def isdecimal(string):
    try:
        Decimal(string)
        return True
    except:
        return False
