from django.db import models
from django.contrib.auth.models import User


CREDITDEBIT_CHOICES = (
    ('credit','Credit'),
    ('debit','Debit'),
)

USE_CHOICES = (
    ('household','Household'),
    ('personal','Personal'),
)

MONEY_CHOICES = (
    ('khata','Khata'),
    ('own','Own'),
)

class Creditdebit(models.Model):
    description = models.TextField()
    rupees =  models.IntegerField()
    pub_datetime = models.DateTimeField()    
    credit_or_debit = models.CharField(max_length=6, choices=CREDITDEBIT_CHOICES, default='Credit')
    used_for = models.CharField(max_length=15, choices=USE_CHOICES, default='Household')
    money_source = models.CharField(max_length=15, choices=MONEY_CHOICES, default='Khata')
    hunter = models.ForeignKey(User, on_delete=models.CASCADE)
    remaining_bal = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    last_edited_date = models.DateTimeField()

    def __str__(self):
        return self.description

class Dashboard(models.Model):
    source_id = models.IntegerField()
    username = models.TextField()
    descript = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    flag_on_off = models.BooleanField(default=1)
    give_take = models.BooleanField(default=1)

    def __str__(self):
        return self.descript

class Inv_equ(models.Model):
    user_name = models.TextField()
    amount = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)

    def __str__(self):
        return self.user_name

