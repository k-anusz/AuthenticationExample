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
