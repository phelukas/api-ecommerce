from django.db import models
from users.models import User
from django.utils.translation import gettext_lazy as _


class ProductCategory(models.Model):
    name = models.CharField("Nome da categoria", max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Categoria do Produto')
        verbose_name_plural = _('Categoria dos Produtos')

    def __str__(self):
        return self.name


class Product(models.Model):
    seller = models.ForeignKey(
        User, related_name="products", on_delete=models.CASCADE)
    category = models.ForeignKey(
        ProductCategory, related_name="product_list", on_delete=models.SET_NULL, null=True)
    name = models.CharField("Nome do produto", max_length=200)
    desc = models.TextField("Descrição", blank=True)
    price = models.DecimalField("Preço", decimal_places=2, max_digits=10)
    quantity = models.IntegerField("Quantidade", default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return self.name
