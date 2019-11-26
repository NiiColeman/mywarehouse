from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
# Create your models here.
from departments.models import Department
from django.shortcuts import reverse
from django.utils import timezone


from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(
            self, username, email, first_name, last_name, password=None,
            commit=True):
        """
        Creates and saves a User with the given email, first name, last name
        and password.
        """
        if not username:
            raise ValueError(_('Users must have username'))
        if not email:
            raise ValueError(_('Users must have an email address'))
        if not first_name:
            raise ValueError(_('Users must have a first name'))
        if not last_name:
            raise ValueError(_('Users must have a last name'))

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email, first name,
        last name and password.
        """
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            commit=False,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True, null=True)

    email = models.EmailField(
        verbose_name=_('email address'), max_length=255, unique=True
    )
    # password field supplied by AbstractBaseUser
    # last_login field supplied by AbstractBaseUser
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )
    # is_superuser field provided by PermissionsMixin
    # groups field provided by PermissionsMixin
    # user_permissions field provided by PermissionsMixin

    date_joined = models.DateTimeField(
        _('date joined'), default=timezone.now
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return '{} <{}>'.format(self.get_full_name(), self.email)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    def get_absolute_url(self):
        return reverse("user_detail", kwargs={"pk": self.pk})
    

class Category(models.Model):
    name = models.CharField(max_length=250)

    # TODO: Define fields here

    class Meta:
        """Meta definition for Category."""

        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        """Unicode representation of Category."""
        return self.name

    def get_absolute_url(self):
        return reverse("items:category_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("items:update_category", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("items:category_delete", kwargs={"pk": self.pk})


class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='images/',null=True,blank=True)
    category = models.ForeignKey(
        Category, related_name='categories', on_delete=models.CASCADE)
    stock_on_hand = models.IntegerField(default=0)
    expiry_date = models.DateField(auto_now=False)
    shelf_number = models.CharField(max_length=50)
    description = models.CharField(max_length=450)
    perishable = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)

    # TODO: Define fields here

    class Meta:
        """Meta definition for Item."""

        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def __str__(self):
        """Unicode representation of Item."""
        return self.name

    def get_absolute_url(self):
        return reverse("items:item_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("items:item_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("items:item_delete", kwargs={"pk": self.pk})


class ItemSetting(models.Model):
    CHOICES = (
        (30, ("1 Months")),
        (60, ("2 Months")),
        (90, ("3 Months")),
        (120, ("4 Months"))

    )
    name = models.CharField(default="Item Settings", max_length=50)
    low_stock_limit = models.IntegerField(default=10)
    item_expiration_limit = models.IntegerField(choices=CHOICES, default=30)

    class Meta:
        verbose_name = ("Item Setting")
        verbose_name_plural = ("Item Settings")

    def __str__(self):
        return self.name


class StoreItem(models.Model):
    name = models.CharField(max_length=250)
    quantity = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True)

    """Model definition for StoreItem."""

    # TODO: Define fields here

    class Meta:
        """Meta definition for StoreItem."""

        verbose_name = 'StoreItem'
        verbose_name_plural = 'StoreItems'

    def __str__(self):

        return self.name
