from django.db import models
from empresa.models import empresa
# Create your models here.
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    empresa = models.ForeignKey(empresa, on_delete=models.CASCADE, null=True, blank=True)
    periodo = models.IntegerField(null=True, blank=True)