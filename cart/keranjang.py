from decimal import Decimal
from django.conf import settings
from website.models import Produk


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, produk, quantity=1, update_quantity=False):
        produk_id = str(produk.id)
        if produk_id not in self.cart:
            self.cart[produk_id] = {'quantity': 0, 'price': int(produk.setela_diskon)}
        if update_quantity:
            self.cart[produk_id]['quantity'] = quantity
        else:
            self.cart[produk_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, produk):
        produk_id = str(produk.id)
        if produk_id in self.cart:
            del self.cart[produk_id]
            self.save()

    def __iter__(self):
        produk_ids = self.cart.keys()
        produks = Produk.objects.filter(id__in=produk_ids)
        for produk in produks:
            self.cart[str(produk.id)]['produk'] = produk

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
