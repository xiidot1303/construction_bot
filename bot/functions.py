from app.models import Client
from functions.get_currency import currency
def is_float(msg):
    try:
        a = float(msg)
        return True
    except:
        return False

#def plot_or_flat(name):
#    obj = Client.objects.get()
def summ_to_dollar(value):
    r = float(value) / round(currency(), 4)
    return round(r, 2)

def dollar_to_summ(value):
    r = float(value) * round(currency(), 4)
    return r
    