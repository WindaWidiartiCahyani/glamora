# Generated by Django 5.0.1 on 2024-06-18 14:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0015_rename_setelah_diskon_produk_setela_diskon'),
        ('website', '0005_chatid_statis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailtransaksi',
            name='produk',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.produk'),
        ),
        migrations.AlterModelOptions(
            name='detailtransaksi',
            options={'verbose_name_plural': 'Detail Transaksi'},
        ),
        migrations.DeleteModel(
            name='Produk',
        ),
    ]
