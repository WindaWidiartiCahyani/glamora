# Generated by Django 4.2.2 on 2023-06-19 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_remove_transaksi_jam_booking_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaksi',
            name='keterangan_pesanan',
            field=models.CharField(blank=True, choices=[('Jemput', 'Jemput'), ('Antar', 'Antar')], max_length=200, null=True),
        ),
    ]
