# import json
# import datetime
# import urllib.request
# from django.conf import settings
# from django.views.generic import View
# from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from website.models import Produk
from .models import Transaksi, DetailTransaksi
from .keranjang import Cart
from .forms import CartAddProdukForm
from django.contrib.auth.decorators import login_required
from website.decorators import ijinkan_pengguna,pilihan_login

@require_POST
def cart_add(request, produk_id):
    cart = Cart(request)  # create a new cart object passing it the request object 
    produk = get_object_or_404(Produk, id=produk_id) 
    quantity = int(request.POST.get('quantity'))
    form = CartAddProdukForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(produk=produk, quantity=quantity, update_quantity=cd['update'])
    return redirect('cart_detail')

def cart_remove(request, produk_id):
    cart = Cart(request)
    produk = get_object_or_404(Produk, id=produk_id)
    cart.remove(produk)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    context = {
            'judul': 'Halaman Cart',
            'cart':cart
        }
    
    for item in cart:
        item['update_quantity_form'] = CartAddProdukForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request,'pemesanan.html',context)

