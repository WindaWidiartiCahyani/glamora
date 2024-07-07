from django.db import models
from website.models import Produk, Custumer
from ckeditor.fields import RichTextField
from django_resized import ResizedImageField
from django import template
from django.contrib.humanize.templatetags.humanize import intcomma



class Transaksi(models.Model):
    Status=(
        ('Belum Lunas', 'Belum Lunas'),
        ('Lunas' , 'Lunas'),
        ('Pengiriman' , 'Pengiriman'),
        ('Selesai' , 'Selesai'),
        ('Batalkan' , 'Batalkan'),
        ('Kadaluarsa' , 'Kadaluarsa'),
        ('Pembayaran Ditolak' , 'Pembayaran Ditolak'),
    )
    KT=(
        ('Jemput', 'Jemput'),
        ('Antar' , 'Antar'),
    )
    custumer = models.ForeignKey(Custumer, null=True, blank=False, on_delete=models.SET_NULL)
    no_transaksi = models.CharField(max_length=200, blank=False, null=True)
    keterangan_pesanan = models.CharField(max_length=200, blank=True, null=True, choices=KT)
    status = models.CharField(max_length=200, default="Belum Lunas", blank=True, null=True, choices=Status)
    total_transaksi = models.BigIntegerField(blank=True, null=True)
    date_created= models.DateTimeField(auto_now_add=True, null=True,blank=True)
    token_payment = models.CharField(max_length=300, blank=True, null=True)


    # @property
    # def tanggal_pengiriman(self):
    #     if self.tanggal_kirim is None:
    #         tglkirim ="-"
    #     else:
    #         tglkirim = self.tanggal_kirim.strftime("%d %b %Y %H:%M:%S")
    #     return tglkirim

    class Meta:
        ordering = ('-no_transaksi', )

    def __str__(self):
         return f"{self.no_transaksi}-({self.total_transaksi})" 
    
    class Meta:
        verbose_name_plural ="Transaksi"

    @property
    def total_pemabayaran(self):
        hargavalid = str(self.total_transaksi).replace('.0','')
        hargafik = int(hargavalid)
        hargarupiah = intcomma(hargafik)
        fikharga =  f"Rp. {str(hargarupiah)}"
        return fikharga
    
class DetailTransaksi(models.Model):
    no_transaksi = models.CharField(max_length=200, blank=False, null=True)
    produk = models.ForeignKey(Produk, null=True, on_delete=models.SET_NULL)
    jumlah = models.IntegerField(blank=True, null=True)
    
    class Meta:
        ordering = ('-no_transaksi', )
        

    def __str__(self):
         nilai = str(self.produk.setela_diskon)
         hargavalid = (nilai.replace(".0",""))
         return f"No Transaksi: {self.no_transaksi} Produk: ({self.produk}) Jumlah: ({self.jumlah})  Harga: ({hargavalid})" 
    
    @property
    def harga(self):
        total = self.produk.setela_diskon 
        hargavalid = str(total).replace('.0','')
        hargafik = int(hargavalid)
        hargarupiah = intcomma(hargafik)
        fikharga =  f"Rp. {str(hargarupiah)}"


        return fikharga

    @property
    def sub_total(self):
        total = self.produk.setela_diskon * self.jumlah

        hargavalid = str(total).replace('.0','')
        hargafik = int(hargavalid)
        hargarupiah = intcomma(hargafik)
        fikharga =  f"Rp. {str(hargarupiah)}"


        return fikharga
    class Meta:
        verbose_name_plural ="Detail Transaksi"

