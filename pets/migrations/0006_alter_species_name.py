# Generated by Django 4.0.6 on 2022-08-02 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0005_remove_pet_adopted_owner_file_pet_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='species',
            name='name',
            field=models.CharField(choices=[('cat', 'Cat'), ('dog', 'Dog'), ('rabbit', 'Rabbit'), ('hamster', 'Hamster'), ('bird', 'Birds')], max_length=100),
        ),
    ]
