# Generated by Django 3.0.4 on 2020-03-10 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, verbose_name='Nombre de la Empresa')),
                ('razon', models.CharField(max_length=255, verbose_name='Razón Social')),
                ('ruc', models.CharField(max_length=12, verbose_name='Numero de RUC')),
                ('contacto', models.CharField(max_length=255, verbose_name='Contacto')),
                ('correo', models.EmailField(max_length=254, verbose_name='Correo Electronico')),
                ('icono', models.ImageField(blank=True, null=True, upload_to='Empresas', verbose_name='Icono de la Empresa')),
            ],
        ),
    ]
