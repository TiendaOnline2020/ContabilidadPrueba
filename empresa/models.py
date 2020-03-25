from django.db import models

# Create your models here.

class empresa(models.Model):
    nombre = models.CharField(max_length=255,verbose_name="Nombre de la Empresa")
    razon = models.CharField(max_length=255, verbose_name="Razón Social")
    ruc = models.CharField(max_length=12, verbose_name="Numero de RUC")
    contacto = models.CharField(max_length=255, verbose_name="Contacto")
    correo = models.EmailField(verbose_name="Correo Electronico")
    icono = models.ImageField(null=True, verbose_name="Icono de la Empresa",upload_to="Empresas",blank=True)

    def __str__(self):
        return self.nombre