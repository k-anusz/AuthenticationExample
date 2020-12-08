from django.db import models


# Create your models here.

# This is our table in our database, it allows us to store a bunch of city names in the table
class City(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    # This meta class is so that the plural of city will be cities with "ies" instead of citys with "s"
    # this is helpful for visual display when using the admin dashboard
    class Meta:
        verbose_name_plural = 'cities'


# This is our table in our database, it allows us to store a bunch of bank names and balance in the table
class Bank(models.Model):
    userId = models.IntegerField(default=73)
    bankName = models.CharField(max_length=50)
    balance = models.FloatField(default=0.0)
    startBal = models.FloatField(default=0.0)


# This is our table in our database, it allows us to store a bunch of
# bank account transactions names and amounts in the table
class BankAccount(models.Model):
    bankId = models.IntegerField(default=73)
    transactionName = models.CharField(max_length=50)
    transactionAmount = models.FloatField(default=0.0)
    transaction_date = models.DateTimeField(auto_now_add=True, blank=True)








