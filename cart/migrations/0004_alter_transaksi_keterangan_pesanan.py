# Generated by Django 4.2.2 on 2023-06-19 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_alter_transaksi_keterangan_pesanan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaksi',
            name='keterangan_pesanan',
            field=models.CharField(blank=True, choices=[('Jemput', 'Jemput'), ('Antar', 'Antarz')], max_length=200, null=True),
        ),
    ]