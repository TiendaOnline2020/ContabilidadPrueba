from django.contrib import admin
from .models import detalle
from documento.models import documento


# Register your models here.
class Admin_Documento(admin.ModelAdmin):
    fields = (
        'descripcion',
        ('cantidad', 'monto')
    )
    '''
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'documento':
            kwargs['queryset'] = documento.objects.filter(empresa=request.user.empresa).order_by('empresa__nombre')
        return super(Admin_Documento, self).formfield_for_foreignkey(db_field, request, **kwargs)
    '''

admin.site.register(detalle, Admin_Documento)
