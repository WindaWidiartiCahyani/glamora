from django.db import models
from PIL import Image
# from ckeditor.fields import RichTextField
from django_resized import ResizedImageField
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Kategori(models.Model):
    nama = models.CharField(max_length=200, blank=False, null=True,verbose_name="Nama Kategori")
    aktif = models.BooleanField(default=True)
   
    slug = models.SlugField(max_length=200, null=False, unique=True)

    @property
    def get_produk(self):
        return Produk.objects.filter(kategori__nama=self.nama)
    
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.nama)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nama
    
    class Meta:
        verbose_name_plural ="Kategori"


class Produk(models.Model):

    kategori = models.ForeignKey(Kategori, null=True, blank=False, related_name="produk", on_delete=models.SET_NULL)
    nama_produk = models.CharField(max_length=200, blank=False, null=True, unique=True)
    gambar = ResizedImageField(size=[600, 600], quality=80, crop=['middle', 'center'] , upload_to='gambar/produk', blank=False, null=True, verbose_name="Gambar (600 x 600 pixel)")
    gambar_satu = ResizedImageField(size=[600, 600], quality=80, crop=['middle', 'center'] , upload_to='gambar/produk', blank=True, null=True, verbose_name="Gambar (600 x 600 pixel)")
    gambar_dua = ResizedImageField(size=[600, 600], quality=80, crop=['middle', 'center'] , upload_to='gambar/produk', blank=True, null=True, verbose_name="Gambar (600 x 600 pixel)")
    gambar_tiga = ResizedImageField(size=[600, 600], quality=80, crop=['middle', 'center'] , upload_to='gambar/produk', blank=True, null=True, verbose_name="Gambar (600 x 600 pixel)")
    gambar_empat = ResizedImageField(size=[600, 600], quality=80, crop=['middle', 'center'] , upload_to='gambar/produk', blank=True, null=True, verbose_name="Gambar (600 x 600 pixel)")
    gambar_lima= ResizedImageField(size=[600, 600], quality=80, crop=['middle', 'center'] , upload_to='gambar/produk', blank=True, null=True, verbose_name="Gambar (600 x 600 pixel)")
    slug = models.SlugField(max_length=200, unique=True)
    keterangan = models.TextField(blank=False, null=True)
    harga = models.PositiveIntegerField(blank=False, null=True)
    no_whatsup = models.PositiveBigIntegerField(blank=False, null=True,)
    tanggal_upload= models.DateTimeField(auto_now_add=True, null=True)
    diskon = models.IntegerField(default=0,  blank=True, null=True, verbose_name="Diskon (%)*)Kosongi")
    stock = models.IntegerField(default=0,  blank=True, null=True)
    dibeli = models.IntegerField(default=0,  blank=True, null=True)


    @property
    def setela_diskon(self):
        if self.diskon == 0 :
            nilai_diskon = self.harga
        else:
            jml = self.diskon / 100
            nilai_diskon = self.harga - (jml * self.harga)
        return nilai_diskon
    
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.nama_produk)
        return super().save(*args, **kwargs)


    def __str__(self):
        return self.nama_produk
    class Meta:
        verbose_name_plural ="Produk"


class Slide(models.Model):
    judul = models.CharField(max_length=200, blank=False, null=True,verbose_name="Judul")
    gambar_slide = models.ImageField(upload_to='gambar/slide', blank=False, null=True, verbose_name="Gambar (1920 x 880 pixel)")
    aktif = models.BooleanField(default=True)

    def __str__(self):
        return self.judul
    class Meta:
        verbose_name_plural ="Slide"
    def save(self, *args, **kwargs):
        super(Slide, self).save(*args, **kwargs)

        img = Image.open(self.gambar_slide.path)

        if img.height > 1920 or img.width > 880:
            output_size = (1920,880)
            img.thumbnail(output_size)
            img.save(self.gambar_slide.path)


# class Testimoni(models.Model):
#     nama = models.CharField(max_length=200, blank=False, null=True,verbose_name="Nama")
#     pekerjaan = models.CharField(max_length=200, blank=False, null=True,verbose_name="Pekerjaan")
#     gambar_testimoni = models.ImageField(upload_to='gambar/testimoni', blank=False, null=True, verbose_name="Gambar (90 x 90 pixel)")
#     deskripsi = models.TextField(blank=False, null=True)
#     aktif = models.BooleanField(default=True)

#     def __str__(self):
#         return self.nama
#     class Meta:
#         verbose_name_plural ="Testimoni"

class Kontak(models.Model):
    nama = models.CharField(max_length=200, blank=False, null=True)
    no_whatsup = models.PositiveBigIntegerField(blank=True, null=True,)
    email = models.EmailField(max_length=200,blank=False, null=True)
    subject = models.CharField(max_length=200, blank=False, null=True)
    isi = models.TextField(max_length=200, blank=False, null=True)

    def __str__(self):
        
        return '%s, %s' % (self.nama, self.email) 
    class Meta:
        verbose_name_plural ="Kontak"


class Profil(models.Model):
    nama = models.CharField(max_length=200, blank=False, null=True)
    keterangan = models.TextField(blank=False, null=True)
    gambar = models.ImageField(upload_to='gambar/profil',blank=True, null=True, verbose_name="Gambar (1920 x 1200 pixel)")
    tanggal_upload= models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return self.nama
    class Meta:
        verbose_name_plural ="Profil"

# class Statis(models.Model):
#     alamat_kami = models.TextField(max_length=200, blank=False, null=True)
#     telpon = models.CharField(max_length=200, blank=False, null=True)
#     email = models.EmailField(max_length=200, blank=False, null=True)
   

#     def __str__(self):
#         return self.email
#     class Meta:
#         verbose_name_plural ="Statis"


class Custumer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    nama = models.CharField(max_length=200, blank=False, null=True)
    wa = models.CharField(max_length=200, blank=False, null=True,verbose_name="No Whatsapp")
    alamat = models.TextField(blank=False, null=True)
    email = models.EmailField(max_length=200, blank=False, null=True)
    date_created= models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.nama
    class Meta:
        verbose_name_plural ="Custumer"

class ChatID(models.Model):
    chatid = models.CharField(max_length=200, blank=False, null=True)
    nama = models.CharField(max_length=200, blank=False, null=True)
    aktif = models.BooleanField(default= True)
    
    class Meta:
        verbose_name_plural ="Chat ID"