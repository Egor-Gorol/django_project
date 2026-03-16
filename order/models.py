from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Нова'),
        ('processing', 'В обробці'),
        ('shipped', 'Відправлено'),
        ('delivered', 'Доставлено'),
        ('canceled', 'Скасовано'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    shipping_name = models.CharField(max_length=255, verbose_name='Ім\'я отримувача')
    shipping_phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    shipping_sity = models.CharField(max_length=100, verbose_name='Місто')
    shipping_street = models.CharField(max_length=255, verbose_name='Вулиця')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    coment = models.TextField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'
        ordering = ['-created_at']

    def __str__(self):
        user_name = self.user.username if self.user else 'guest'
        return f"Order #{self.id} by {user_name} created on {self.created_at}"
    


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity} x {self.product_name} in Order #{self.order.id}"
