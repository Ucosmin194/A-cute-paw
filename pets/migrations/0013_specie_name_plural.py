# Generated by Django 4.0.6 on 2022-08-04 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0012_specie_navbar_promo'),
    ]

    operations = [
        migrations.AddField(
            model_name='specie',
            name='name_plural',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
