# Generated by Django 4.0.6 on 2022-08-18 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0023_alter_adoptionrequest_confirmed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adoptionrequest',
            name='confirmed',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]