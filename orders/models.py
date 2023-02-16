from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property

from users.models import User, Address
from products.models import Product


class Order(models.Model):
    PENDING = 'P'
    COMPLETED = 'C'

    STATUS_CHOICES = ((PENDING, _('Pendente')), (COMPLETED, _('Completa')))

    buyer = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    status = models.CharField("Status", max_length=1,choices=STATUS_CHOICES, default=PENDING)
    shipping_address = models.ForeignKey(Address, related_name='shipping_orders', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(Address, related_name='billing_orders', on_delete=models.SET_NULL, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return self.buyer.get_full_name()

    @cached_property
    def total_cost(self):
        """Custo total de todos os itens em um pedido"""
        return round(sum([order_item.cost for order_item in self.order_items.all()]), 2)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="product_orders", on_delete=models.CASCADE)
    quantity = models.IntegerField("Quantidade")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return self.order.buyer.get_full_name()

    @cached_property
    def cost(self):
        """Custo total do item pedido"""
        return round(self.quantity * self.product.price, 2)
