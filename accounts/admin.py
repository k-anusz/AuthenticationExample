from django.contrib import admin
from .models import City
from .models import BankAccount
from .models import Bank

# Register your models here.
# Here we are adding City to the admin dashboard
admin.site.register(City)
admin.site.register(Bank)
admin.site.register(BankAccount)
