from django.db import models


# Create your models here.
'''
3.	modelo detalle:  un campo vinculado  mucho a muchos con  la tabla documento
   t.text     "descripcion"
    t.float    "cantidad"
    t.float    "precio"  * es calculado monto / cantidad
    t.float    "monto"
'''


class detalle(models.Model):
    descripcion = models.TextField(null=True, blank=True)
    cantidad = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Cantidad")
    monto = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Monto')
    precio = models.DecimalField(max_digits=20, decimal_places=2)

    def save(self, *args, **kwargs):
        self.precio = self.monto / self.cantidad
        super(detalle, self).save(*args, **kwargs)
