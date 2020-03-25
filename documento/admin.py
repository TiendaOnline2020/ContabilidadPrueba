from django.contrib import admin
from .models import documento
# Register your models here.
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter
from detalle.models import detalle

class StatusFilter(SimpleListFilter):
    title = _('Tipo de Cambio')

    parameter_name = 'opciones'

    def lookups(self, request, model_admin):
        return (
            (None, _('Todos')),
            ('compra', _('Compra')),
            ('venta', _('Venta')),
        )

    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        if self.value() in ('compra', 'venta'):
            if self.value() == 'compra':
                return queryset.filter(empresa=request.user.empresa,tipo_cambio=str(self.value()))
            return queryset.filter(empresa=request.user.empresa, tipo_cambio=str(self.value()))
        elif self.value() == None:
            return queryset.filter(empresa=request.user.empresa)

class Admin(admin.ModelAdmin):
    list_display = ('n_documento', 'ruc', 'razon_social', 'empresa','tipo_cambio','tc','monto')
    def save_model(self, request, obj, form, change):
        obj.empresa = request.user.empresa
        super(Admin, self).save_model(request, obj, form, change)
    fields = (
        'periodo',
        'serie',
        'n_documento',
        ('ruc', 'actualizar_ruc'),
        'documento',
        ('moneda','tipo_cambio'),
        ('fecha','tc','actualizar_tc'),
    )
    list_filter = [StatusFilter]
    actions = ['Actualizar_Monto']
    def Actualizar_Monto(self, request, queryset):
        for objeto in queryset:
            detalles = detalle.objects.filter(documento=objeto)
            monto_total = 0
            for detalle_objeto in detalles:
                monto_total += detalle_objeto.monto
            objeto.monto = monto_total
            objeto.primer_gurdado = False
            objeto.actualizar_ruc = False
            objeto.actualizar_tc = False
            objeto.save()
    Actualizar_Monto.allow_tags = True
    Actualizar_Monto.short_description = 'Actualizar Montos'
    date_hierarchy = 'periodo'

admin.site.register(documento, Admin)