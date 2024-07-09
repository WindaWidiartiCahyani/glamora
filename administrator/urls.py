from django.urls import path
from . import views



urlpatterns = [
    path('', views.beranda_admin, name='beranda_admin'),

    path('kategori-admin/', views.kategori_admin, name='kategori_admin'),
    path('form-kategori/', views.formkategori_admin, name='formkategori_admin'),
    path('edit-kategori/<str:slug>', views.editkategori_admin, name='editkategori_admin'),
    path('delete-kategori/<str:pk>', views.deletekategori_admin, name='deletekategori_admin'),
    
    path('produk-admin/', views.produk_admin, name='produk_admin'),
    path('form-produk/', views.formproduk_admin, name='formproduk_admin'),
    path('edit-produk/<str:slug>', views.editproduk_admin, name='editproduk_admin'),
    path('delete-produk/<str:pk>', views.deleteproduk_admin, name='deleteproduk_admin'),

    path('slide-admin/', views.slide_admin, name='slide_admin'),
    path('form-slide/', views.formslide_admin, name='formslide_admin'),
    path('edit-slide/<str:pk>', views.editslide_admin, name='editslide_admin'),
    path('delete-slide/<str:pk>', views.deleteslide_admin, name='deleteslide_admin'),

    path('kontak/', views.kontak_admin, name='kontak_admin'),
 
    path('laporan/', views.laporan, name='laporan'),
    path('transaksi/', views.transaksi_list, name='transaksi_list'),
    path('transaksi/detail/<str:notransaksi>/', views.detail_transaksi, name='detail_transaksi'),

    path('custumer-admin/', views.custumer_admin, name='custumer_admin'),
    path('delete-custumer/<str:pk>', views.deletecustumer_admin, name='deletecustumer_admin'),
    
    path('export-laporan/', views.export_laporan, name='export_laporan'),
]
  
