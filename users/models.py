from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext as _
from django.db import models


class UsuarioManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    first_name = models.CharField(
        "Primeiro nome", max_length=20, blank=False, null=False)
    last_name = models.CharField(
        "Segundo nome", max_length=20, blank=False, null=False)
    is_staff = models.BooleanField('Membro da equipe', default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
        'is_staff'
    ]

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    objects = UsuarioManager()


class Address(models.Model):
    BILLING = 'C'
    SHIPPING = 'E'

    ADDRESS_CHOICES = ((BILLING, _('cobrança')), (SHIPPING, _('envio')))

    user = models.ForeignKey(
        User, related_name='addresses', on_delete=models.CASCADE)
    address_type = models.CharField(
        "Tipo do endereço", max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField("Endereço principal?", default=False)
    country = models.CharField("País", max_length=100)
    city = models.CharField("Cidade", max_length=100)
    street_address = models.CharField("Rua", max_length=100)
    postal_code = models.CharField("CEP", max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.user}: {self.street_address} - {self.city}'


class PhoneNumber(models.Model):
    user = models.OneToOneField(User, related_name='phone', on_delete=models.CASCADE)
    phone_number = models.CharField("Numero telefone", unique=True, max_length=15)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return self.phone_number
