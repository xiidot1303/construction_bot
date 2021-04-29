from app.models import Client

def is_float(msg):
    try:
        a = float(msg)
        return True
    except:
        return False

#def plot_or_flat(name):
#    obj = Client.objects.get()