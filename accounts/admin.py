from django.contrib import admin
from .models import City

# Register your models here.
# Here we are adding City to the admin dashboard
admin.site.register(City)