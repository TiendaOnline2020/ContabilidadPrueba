from django.db import models
from django.http import Http404

from empresa.models import empresa
# Create your models here.
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import requests

def validar_ruc(value):
    try:
        a = str(int(value))
        if not len(a) == 11:
            raise ValidationError('No es un numero RUC')
    except ValueError:
        raise ValidationError('Admite numeros')
def verificar_fecha(value):
    from datetime import date
    fecha = date.today()
    if fecha<value:
        raise ValidationError('Fecha no admitida')
    elif fecha == value:
        raise ValidationError('No es posible la facha actual')
    dia = int(value.strftime('%d'))
    mes = int(value.strftime('%m'))
    year = int(value.strftime('%Y'))
    if year < 1583:
        raise ValidationError('Solo acepta fechas mayores a 1582')
    else:
        a = (14 - mes) // 12
        y = year - a
        m = mes + 12 * a - 2
        d = (dia + year + (year // 4) - (year // 100) + (year // 400) + ((31 * m) // 12)) % 7
        if d == 0:
            raise ValidationError('La fecha no puede ser Domingo')
        elif d == 1:
            raise ValidationError('La fecha no puede ser Lunes')

tipo_documento = (
    ('factura','Factura'),
    ('boleta','Boleta'),
    ('comprobante','Comprobante'),
    ('nota_de_credito','Nota de Credito'),
    ('nota_de_debito','Nota de Debito')
)
tipo_moneda = (
    ('soles','Soles'),
    ('dolar','Dolar'),
    ('euro','Euro'),
)
tipo_cambio_choices = (
    ('compra','Compra'),
    ('venta','Venta')
)





class documento(models.Model):
    periodo = models.DateField(auto_now=False, auto_now_add=False)
    serie = models.CharField(max_length=255)
    n_documento = models.CharField(max_length=255, verbose_name="Nº Documento")
    ruc = models.CharField(max_length=12, verbose_name="RUC", validators=[validar_ruc])
    monto = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    documento = models.CharField(max_length=50, choices=tipo_documento, null=True, blank=True)
    moneda = models.CharField(max_length=50, choices=tipo_moneda, default="soles")
    fecha = models.DateField(auto_now=False, auto_now_add=False,validators=[verificar_fecha])
    tc = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name='Valor TC')
    tipo_cambio = models.CharField(max_length=255, choices=tipo_cambio_choices,verbose_name="Tipo de Cambio")
    actualizar_tc = models.BooleanField(default=True)
    empresa = models.ForeignKey(empresa, null=True, on_delete=models.CASCADE)
    razon_social = models.CharField(max_length=255, verbose_name="Razon Social")
    actualizar_ruc = models.BooleanField(default=True)
    primer_gurdado = models.BooleanField(default=True)
    def __str__(self):
        return self.n_documento
    def save(self, *args, **kwargs):
        if self.primer_gurdado:
            from detalle.models import detalle
            detalles = detalle.objects.filter(documento__id=self.id)
            if len(detalles)>0:
                print(len(detalles + "esto es"))
                total_pagar = 0
                for detalle_objeto in detalles:
                    total_pagar += detalle_objeto.monto
                self.monto = total_pagar
                self.primer_gurdado = False
            else:
                self.monto = None
        if self.actualizar_ruc:
            url = settings.URL_API_SUNAT
            url += self.ruc
            try:
                informacion = requests.get(url).json()
                self.razon_social = informacion['razon_social']
            except:
                raise Http404
            self.actualizar_ruc = False
        if self.moneda == 'dolar':
            if self.actualizar_tc:
                url = settings.URL_TIPO_CAMBIO_SUNAT
                url += str(self.fecha)
                print(url)
                fecha_str = ""+str(self.fecha)+""
                informacion = requests.get(url).json()
                print(informacion)
                compra_venta = informacion[fecha_str]
                print(compra_venta)
                if self.tipo_cambio == 'compra':
                    self.tc = float(compra_venta['compra'])
                else:
                    self.tc = float(compra_venta['venta'])
        super(documento, self).save(*args, **kwargs)
