from django.db import models

from loggi.models import Father

# Create your models here.

class Son(models.Model):
    father = models.ForeignKey(Father, on_delete=models.CASCADE)

