# Generated by Django 3.2 on 2023-01-19 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0003_alter_itemprice_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='type',
            field=models.CharField(choices=[('hats', 'hats'), ('tops', 'tops'), ('shorts', 'shorts')], default='hats', max_length=150),
        ),
    ]