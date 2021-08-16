from django.db import models
#admin panel
class Object(models.Model):
    title = models.CharField(null=True, blank=False, max_length=100)
    price = models.CharField(null=True, blank=False, max_length=30) #unnessary
    price_summ = models.CharField(null=True, blank=True, max_length=30) #unnessary
    price_dollar = models.CharField(null=True, blank=True, max_length=30) #unnessary
    price_material_summ = models.CharField(null=True, blank=True, max_length=30)
    price_material_dollar = models.CharField(null=True, blank=True, max_length=30)
    price_salary_summ = models.CharField(null=True, blank=True, max_length=30)
    price_salary_dollar = models.CharField(null=True, blank=True, max_length=30)
    def __str__(self):
        return self.title

class Foreman(models.Model):
    name = models.CharField(null=True, blank=False, max_length=100)
    login = models.CharField(null=True, blank=False, max_length=100)
    password = models.CharField(null=True, blank=False, max_length=100)
    obj = models.ManyToManyField('Object')
    account_summ = models.CharField(null=True, max_length=100)
    account_dollar = models.CharField(null=True, max_length=100)


class Client(models.Model):
    name = models.CharField(null=True, blank=False, max_length=100)
    login = models.CharField(null=True, blank=False, max_length=100)
    password = models.CharField(null=True, blank=False, max_length=100)
    obj = models.ManyToManyField('Object')
    type = models.CharField(null=True, blank=True, max_length=20) 


class Material(models.Model):
    user_id = models.IntegerField(null=True, blank=True)
    title = models.CharField(null=True, blank=True, max_length=200)
    measurement = models.CharField(null=True, blank=True, max_length=30)
    amount = models.CharField(null=True, blank=True, max_length=30)
    summ_or_dollar = models.CharField(null=True, blank=True, max_length=50)
    price = models.CharField(null=True, blank=True, max_length=30)
    obj = models.CharField(null=True, blank=False, max_length=100)
    published = models.DateTimeField(db_index = True, null=True, auto_now_add=True, blank=True)
    type = models.CharField(null=True, blank=True, max_length=20)
    price_dollar = models.CharField(null=True, blank=True, max_length=30)
class Material_title(models.Model):
    title = models.CharField(null=True, max_length=200, verbose_name='Названия')


class Salary(models.Model):
    user_id = models.IntegerField(null=True, blank=True)
    title = models.CharField(null=True, blank=True, max_length=200)
    summ_or_dollar = models.CharField(null=True, blank=True, max_length=50)
    price = models.CharField(null=True, blank=True, max_length=30)
    obj = models.CharField(null=True, blank=False, max_length=100)
    published = models.DateTimeField(db_index = True, null=True, auto_now_add=True, blank=True)
    type = models.CharField(null=True, blank=True, max_length=20)
    price_dollar = models.CharField(null=True, blank=True, max_length=30)

class Salary_title(models.Model):
    title = models.CharField(null=True, max_length=200, verbose_name='Названия')


#bot
class Bot_users(models.Model):
    user_id = models.IntegerField(null=True, blank=False)
    who = models.CharField(null=True, blank=True, max_length=20)   # foreman or client
    login = models.CharField(null=True, blank=True, max_length=100)
    password = models.CharField(null=True, blank=True, max_length=100)



class transfer_money(models.Model):
    user_id = models.IntegerField(null=True, blank=False)
    foreman = models.CharField(null=True, blank=True, max_length=100)
    object = models.CharField(null=True, blank=True, max_length=100)
    summ_or_dollar = models.CharField(null=True, blank=True, max_length=10)
    price = models.CharField(null=True, blank=True, max_length=100)
    transfered = models.CharField(null=True, max_length=10, blank=True)
    published = models.DateTimeField(db_index = True, null=True, auto_now_add=True, blank=True)