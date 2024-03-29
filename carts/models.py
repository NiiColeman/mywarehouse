from django.db import models
from items.models import Item, User
# Create your models here.

# from .managers import Manager


class CartManager(models.Manager):

    def new_or_get(self, request):
        cart_id = request.session.get('cart_id', None)

        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            print('cart exists')

            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()

        else:
            cart_obj = self.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id

        return cart_obj, new_obj

    def new(self, user=None):
        print(user)
        user_obj = None
        if user is not None:
            if user.is_authenticated:

                user_obj = user

        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)
    item = models.ManyToManyField(Item)
    total = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse("Cart_detail", kwargs={"pk": self.pk})
