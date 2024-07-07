from django.shortcuts import render, redirect,get_object_or_404
import urllib.request
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import tolakhalaman_ini, ijinkan_pengguna
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.views.generic import View
from .models import Kategori, Produk, Slide, Kontak, Profil, Custumer, ChatID
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from cart.forms import CartAddProdukForm
from django.core.paginator import Paginator
from django.db.models import Count, Q
from cart.keranjang import Cart
from cart.models import Transaksi, DetailTransaksi
import datetime
import midtransclient
import uuid
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .constants import PAYMENT_STATUS
import hashlib
import hmac
import base64
import json
# from administrator.forms import CustumerForm
from .telegram_utill import send_telegram_message
from django.contrib.humanize.templatetags.humanize import intcomma

# MIDTRANS_CORE = midtransclient.Snap(
#             is_production=not settings.DEBUG,
#             server_key='SB-Mid-server-lYFlujbf6kblULZvgL5BzyAM',
#             client_key='SB-Mid-client-Mwrb_UsPSl3P4h3x',
#     )

snap = midtransclient.Snap(
    is_production=False,
    server_key='SB-Mid-server-KE-PSOL6jjV0cUtGcdmENj9v',
    client_key='SB-Mid-client-YEoBzZnys8k0YOLj',
)
def beranda(request):
    
    jumlahkategori = Kategori.objects.filter(aktif="True").annotate(produk_count=Count('produk')).order_by('-id')
    produkall = Produk.objects.all()
    produkbest = Produk.objects.all().order_by('-dibeli')
    produkdiskon = Produk.objects.all().filter(diskon__gt=0)
    produk_fashion = Produk.objects.filter(kategori__nama='FASHION')
    aksesoris = Produk.objects.filter(kategori__nama='AKSESORIS')  
    slide = Slide.objects.filter(aktif="True").order_by('-id')
    context = {
        'judul': 'Beranda',
        'kategori':jumlahkategori,
        'produkall':produkall,
        'produkbest':produkbest,
        'produkdiskon':produkdiskon,
        'produk_fashion': produk_fashion,
        'aksesoris': aksesoris,
        'slide':slide,
        'menu':'beranda',



    }
    return render(request, 'beranda.html', context)

@tolakhalaman_ini
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.error(request, 'Username Tidak ditemukan')
            return redirect('loginpage')
        
        cocokan = authenticate(request, username=username, password=password)
        if cocokan is None:
            messages.error(request, 'Usernama dana Password yang anda masukan salah')
            return redirect('loginpage')
        if cocokan is not None:
            login(request, cocokan)
            return redirect('beranda_admin')
    context = {
        'judul': 'Login',
    }
    return render(request, 'login.html', context)

def logoutpage(request):
    logout(request)
    return redirect('loginpage') 

@tolakhalaman_ini
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        nama = request.POST['nama']
        wa = request.POST['wa']
        alamat = request.POST['alamat']
        email = request.POST['email']
        group_name = 'custumer'  # Nama grup yang ingin Anda gunakan

        if password != password2:
            messages.error(request, 'Password and Confirm Password do not match.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('register')

        # Simpan user

       
        user = User.objects.create_user(username=username, password=password)
        # Tambahkan data tambahan
        user.first_name = nama
        user.email = email
        user.save()
        pelanggan = Custumer.objects.create(user=user, nama=password, wa=wa, alamat=alamat, email=email)
        # Tambahkan user ke grup
        group = Group.objects.get(name=group_name)
        user.groups.add(group)

        messages.success(request, 'Registration successful. You can now login.')
        return redirect('loginpage')
    else:
        return render(request, 'register.html')

def profil(request):
    profil = Profil.objects.all().order_by('-id')[:1]
    context = {
        'judul': 'Profil Kami',
        'menu':'profil',
        'profil':profil,



    }
    return render(request, 'profil.html', context)


class KontakView(View):
    def get(self, request):
        context = {
        'judul': 'Hubungi Kami',
        'menu':'hubungi',
       }
        return render(request, 'hubungi.html', context)
       
    def post(self, request):
        context = {
           'judul': 'Hubungi Kami',
            'menu':'hubungi',
            'data': request.POST,
            'has_error': False
        }
        nama = request.POST.get('nama')
        no_whatsup = request.POST.get('whatsapp')
        subject = request.POST.get('subject')
        email = request.POST.get('email')
        pesan = request.POST.get('pesan')
        if nama=="":
           messages.error(request, 'Nama Masih kosong')
           context['has_error'] = True

        if no_whatsup=="":
               messages.error(request, 'No whatsapp Masih kosong')
               context['has_error'] = True

        if subject=="":
               messages.error(request, 'Subject Masih kosong')
               context['has_error'] = True

        if pesan=="":
               messages.error(request, 'Pesan Masih kosong')
               context['has_error'] = True

        if context['has_error']:
            return render(request, 'hubungi.html', context, status=400)

        kontak = Kontak.objects.create(nama = nama, email = email, no_whatsup=no_whatsup, subject = subject,  isi = pesan )
        kontak.save()
        context = {
                    'judul': 'Hubungi Kami',
                    'menu':'hubungi',
                    'data': "",
                    'has_error': False
        }
        messages.success(request, 'Pesan sudah terkirim, silakan tunggu respon selanjutnya!')
        return render(request, 'hubungi.html', context, status=400)
    
def produk(request, kategori_slug, slug):
    produk = get_object_or_404(Produk, slug=slug)
    related = Produk.objects.filter(kategori=produk.kategori.id)
    kategori = Kategori.objects.filter(aktif=True)
    produkdiskon = Produk.objects.filter(diskon__gt=0)
    produk_fashion = Produk.objects.filter(kategori__nama='FASHION')  # Filter produk fashion
    aksesoris = Produk.objects.filter(kategori__nama='AKSESORIS')  
    jml = related.count()
    cart_product_form = CartAddProdukForm()
    current_site = get_current_site(request)
    
    context = {
        "judul": "Halaman Produk-Produk",
        "produk": produk,
        "related": related,
        "jml": jml,
        'kategori': kategori,
        "cart_product_form": cart_product_form,
        "domain": current_site.domain,
        'produkdiskon': produkdiskon,
        'aksesoris': aksesoris,
        'produk_fashion': produk_fashion
    }
    return render(request, 'produk.html', context)

@login_required(login_url='loginpage')  
def datapembelian(request):
    id_konsumen = request.user.custumer.id
    # konsumen = Custumer.objects.get(id=id_konsumen)
    transaksi = Transaksi.objects.filter(custumer__id=id_konsumen).order_by('-id')
    context = {
         "judul": "Halaman Pembelian Meubel",
         "transaksi":transaksi
       
    }
    return render(request, 'datapembelian.html', context)

def kategori(request, slug):
    kategori_obj = get_object_or_404(Kategori, slug=slug)
    produk_list = kategori_obj.produk.order_by('-id')  # Akses produk terkait kategori
    cart_product_form = CartAddProdukForm()
    halaman_tampil = Paginator(produk_list, 8)
    halaman_url = request.GET.get('halaman', 1)
    halaman_produk = halaman_tampil.get_page(halaman_url)

    if halaman_produk.has_previous():
        url_previous = f'?halaman={halaman_produk.previous_page_number()}'
    else:
        url_previous = ''

    if halaman_produk.has_next():
        url_next = f'?halaman={halaman_produk.next_page_number()}'
    else:
        url_next = ''
    
    context = {
        "judul": "Halaman Kategori",
        "detailkategori": kategori_obj,
        "produk": halaman_produk,
        'menu': 'produk',
        "previous": url_previous,
        "next": url_next,
        "cart_product_form": cart_product_form,
    }

    return render(request, 'kategori.html', context)
    
def kategoriberanda(request):
    kategori = Kategori.objects.filter(aktif=True).order_by('-id')
    return {'kategori':kategori}



def cari(request):
    datakategori = request.GET.get('kategori')
    datakata = request.GET.get('kata')
    # if datakategori == "all":
    hasilcari = Produk.objects.filter(Q(nama_produk__icontains=datakata)).order_by('-id')
    # else:
        # hasilcari = Produk.objects.filter(Q(nama_produk__icontains=datakata) & Q(kategori__id__exact=datakata)).order_by('-id')
    
    jmlproduk = hasilcari.count()
    context = {
            "judul" : "Halaman Cari",
            "hasilcari" : hasilcari,
            "jmlproduk" : jmlproduk
    }
    print(hasilcari)
    return render(request, 'cari.html', context)


class CheckoutView(View):
    def get(self, request):
        context = {
        'judul': 'Halaman Checkout',
       }
        return render(request, 'checkout.html', context)
       
    def post(self, request):
        id_konsumen = request.user.custumer.id
        konsumen = Custumer.objects.get(id=id_konsumen)
        context = {
            'judul': 'Halaman checkout',
            'data': request.POST,
            'has_error': False
        }
        grantotal = request.POST.get('grantotal')
        keterangan = request.POST.get('keterangan')
        
        no_transaksi = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        if grantotal == "0" :
           messages.error(request, 'Anda belum berbelanja, Silakan belanja terlebih dahulu')
           context['has_error'] = True
        if keterangan=="":
               messages.error(request, 'Keterangan Pengiriman Masih kosong')
               context['has_error'] = True

       

       
        if context['has_error']:
            return render(request, 'checkout.html', context, status=400)

        transaksi = Transaksi.objects.create(no_transaksi = no_transaksi,
                                              custumer = konsumen,
                                              keterangan_pesanan = keterangan,
                                              total_transaksi = grantotal )
        transaksi.save()
        keranjang = Cart(request)
       
        # print(keranjang)
        for r in keranjang:
            
            instance_detail= DetailTransaksi(
                no_transaksi = no_transaksi,
                produk = r['produk'],
                jumlah = r['quantity'],
            )
            instance_detail.save()
            dibeliupdate=Produk.objects.get(nama_produk=r['produk'])
            dibeliupdate.dibeli+=int(r['quantity'])
            dibeliupdate.save()
                
        chats = ChatID.objects.filter(aktif=True)
        for chat in chats:
            grantotal_formatted = f"Rp. {intcomma(grantotal)}"
            message = f"Assalamualaikum Wr Wb,\n\nNo Transaksi: <b>{no_transaksi}</b>\nKeterangan_pesanan: <b>{keterangan}</b>\nCustumer: <b>{konsumen}</b>\nTotal Transaksi:<b>{grantotal}</b>\n\nTerimakasih, Salam Glamora Store dan Wassalamualaikum Wr Wb."
            send_telegram_message(chat.chatid, message)

           

        keranjang.clear()
        messages.success(request, 'Silakan bayar dengan menggunakan VA virtual Account dengan benar dan baik')
        return redirect('datapembelian')
        # context = {
        #             'judul': 'Halaman checkout',
        #             'data': "",
        #             'has_error': False
        # }
        
        # return render(request, 'checkout.html', context, status=400)

def isivitual(request, notransaksi):

    # MIDTRANS_CORE = midtransclient.Snap(
#             is_production=not settings.DEBUG,
#             server_key='SB-Mid-server-lYFlujbf6kblULZvgL5BzyAM',
#             client_key='SB-Mid-client-Mwrb_UsPSl3P4h3x',
#     )
    # midtrans_config = midtransclient.Snap(
    #     server_key='SB-Mid-server-lYFlujbf6kblULZvgL5BzyAM',
    #     client_key='SB-Mid-client-Mwrb_UsPSl3P4h3x',
    #     is_production=not settings.DEBUG
    # )
    # snap = midtransclient(midtrans_config)

    # snap = midtransclient.Snap(
    #         is_production=False,
    #         server_key='SB-Mid-server-lYFlujbf6kblULZvgL5BzyAM',
    #         client_key='SB-Mid-client-Mwrb_UsPSl3P4h3x',
    # )

    # snap = midtransclient.Snap(config=midtrans_config)

    # midtrans_api = midtransclient.CoreApi(midtrans_config)



    transaksi = Transaksi.objects.get(no_transaksi=notransaksi)
    token_payment = uuid.uuid4().hex 
    detail = DetailTransaksi.objects.filter(no_transaksi=notransaksi)
    transaksi.token_payment = token_payment
    transaksi.save()
    item_details = []
    for row in detail:
        item_detail = {
            'id': row.id,
            'price': row.harga,
            'quantity': row.jumlah,
            'name': row.produk.nama_produk,
           
        }
        item_details.append(item_detail)
 
    

    transaction_details = {
        # 'order_id': uuid.uuid4().hex,
        'order_id': token_payment,
        'gross_amount': transaksi.total_transaksi,
    }
    customer_details = {
        'first_name': transaksi.custumer.nama,
        'email': transaksi.custumer.email,
        'phone':transaksi.custumer.wa,
    }
    transaction_data = {
        'transaction_details': transaction_details,
        'item_details': item_details,
        'customer_details': customer_details,
       
    }
  
    response = snap.create_transaction(transaction_data)
     # Buat transaksi dengan Midtrans Snap
    # transaction = snap.create_transaction(payload)

    # Ambil token pembayaran dari response
    # payment_token = response['token']
    transaction_token = response['token']
    transaction_redirect_url = response['redirect_url']

    context = {
         "judul": "Halaman Payment Gateway",
        #  'payment_url': response['redirect_url']
        #  'payment_url': payment_token 
        'url':transaction_redirect_url,
         'token':transaction_token,
          'transaksi':transaksi,
        'detail':detail

         
     
    }
    return render(request, 'va.html', context)
@csrf_exempt
def midtrans_callback(request):
    if request.method == 'POST':
        # Ambil data callback dari Midtrans
        data = request.POST['result_data']
        hasil = json.loads(data)
        print(hasil)

        order_id = hasil['order_id']
        print(order_id)
        
        transaction_status = PAYMENT_STATUS[hasil['transaction_status']]
        transaction = Transaksi.objects.get(token_payment=order_id)
        transaction.status = transaction_status
        transaction.save()

        # Lakukan tindakan tambahkan sesuai kebutuhan aplikasi, contoh:
        if transaction_status == 'Lunas':

            detailtransaksi = DetailTransaksi.objects.values('jumlah','produk__id').filter(no_transaksi=transaction.no_transaksi)
            for detail in detailtransaksi:
                produk = Produk.objects.get(id=detail['produk__id'])
                produk.stock -= detail['jumlah']
                produk.dibeli += detail['jumlah']
                produk.save()
          

    # Jika request bukan POST, kembalikan respons 400 (Bad Request)
    context = {
         "judul": "Halaman Keterangan Payment Gateway", 
        'pesan':hasil['status_message'],
       

         
     
    }
    return render(request, 'hasilva.html', context)
    
