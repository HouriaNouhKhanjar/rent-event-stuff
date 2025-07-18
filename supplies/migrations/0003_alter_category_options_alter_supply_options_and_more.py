# Generated by Django 5.2.4 on 2025-07-13 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplies', '0002_alter_supply_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['created_on'], 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='supply',
            options={'verbose_name_plural': 'Supplies'},
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, unique=True),
        ),
    ]
