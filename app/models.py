from django.db import models
#admin panel
class Object(models.Model):
    title = models.CharField(null=True, blank=False, max_length=100)
    price = models.CharField(null=True, blank=False, max_length=30)
    #price_summ = models.CharField(null=True, blank=True, max_length=30)
    #price_dollar = models.CharField(null=True, blank=True, max_length=30)
    def __str__(self):
        return self.title


class Foreman(models.Model):
    name = models.CharField(null=True, blank=False, max_length=100)
    login = models.CharField(null=True, blank=False, max_length=100)
    password = models.CharField(null=True, blank=False, max_length=100)
    obj = models.ManyToManyField('Object')


class Client(models.Model):
    name = models.CharField(null=True, blank=False, max_length=100)
    login = models.CharField(null=True, blank=False, max_length=100)
    password = models.CharField(null=True, blank=False, max_length=100)
    obj = models.ManyToManyField('Object')


class Material(models.Model):
    user_id = models.IntegerField(null=True, blank=True)
    title = models.CharField(null=True, blank=True, max_length=200)
    measurement = models.CharField(null=True, blank=True, max_length=30)
    amount = models.CharField(null=True, blank=True, max_length=30)
    summ_or_dollar = models.CharField(null=True, blank=True, max_length=50)
    price = models.CharField(null=True, blank=True, max_length=30)
    obj = models.CharField(null=True, blank=False, max_length=100)

class Salary(models.Model):
    user_id = models.IntegerField(null=True, blank=True)
    title = models.CharField(null=True, blank=True, max_length=200)
    summ_or_dollar = models.CharField(null=True, blank=True, max_length=50)
    price = models.CharField(null=True, blank=True, max_length=30)
    obj = models.CharField(null=True, blank=False, max_length=100)




#bot
class Bot_users(models.Model):
    user_id = models.IntegerField(null=True, blank=False)
    who = models.CharField(null=True, blank=True, max_length=20)   # foreman or client
    login = models.CharField(null=True, blank=True, max_length=100)
    password = models.CharField(null=True, blank=True, max_length=100)

