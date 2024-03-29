from django.shortcuts import render
from .models import Cart
# Create your views here.


def cart_create(user=None):
    cart_obj = Cart.objects.create(user=None)
    return cart_obj


def cart_home(request):
    # del request.session['cart_id']
    # request.session['cart_id'] = "12"
    # cart_id = request.session.get('cart_id', None)

    # qs = Cart.objects.filter(id=cart_id)
    # if qs.count() == 1:
    #     print('cart exists')

    #     cart_obj = qs.first()
    #     if request.user.is_authenticated and cart_obj.user is None:
    #         cart_obj.user=request.user
    #         cart_obj.save()

    # else:
    #     cart_obj = Cart.objects.new(user=request.user)
    #     request.session['cart_id'] = cart_obj.id
    cart_obj = Cart.objects.new_or_get(request)

    return render(request, "carts/home.html", {})
