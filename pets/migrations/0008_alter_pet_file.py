# Generated by Django 4.0.6 on 2022-08-02 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0007_alter_pet_species_delete_species'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='file',
            field=models.ImageField(null=True, upload_to='static/image/pets'),
        ),
    ]