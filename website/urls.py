from django.urls import path
from .import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('login/', views.loginpage, name='loginpage'),
    path('register/', views.register, name='register'),
    path('logout/', views.logoutpage, name='logoutpage'),
    path('', views.beranda, name='beranda'),
    path('profil/', views.profil, name='profil'),
    path('hubungi/', views.KontakView.as_view(), name='hubungi'),
    path('cari/', views.cari, name='cari'),
    path('<slug:kategori_slug>/<slug:slug>', views.produk, name='produk'),
    path('<slug:slug>', views.kategori, name='kategori'),
    path('checkout/', login_required(login_url='loginpage')(views.CheckoutView.as_view()), name='checkout'),
    path('isi-vitual-account/<str:notransaksi>/', views.isivitual, name='isivitual'),
    path('data-pembelian/', views.datapembelian, name='datapembelian'),
    path('midtrans_callback/', views.midtrans_callback, name='midtrans_callback'),
]