# Generated by Django 5.0.1 on 2024-07-18 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0016_alter_detailtransaksi_produk_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaksi',
            name='alamat_kirim',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='transaksi',
            name='wa_kirim',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='No Whatsapp'),
        ),
    ]
