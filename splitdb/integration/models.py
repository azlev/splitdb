from django.db import models

from db import SpanningForeignKey
from loggi.models import Father

# Create your models here.

class Son(models.Model):
    father = SpanningForeignKey(Father, on_delete=models.CASCADE)

