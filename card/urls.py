from django.urls import path
from . import views

app_name = 'card'

urlpatterns = [
    path('add/<str:slug>/', views.add_to_cart, name='add_to_cart'),
    path('details/', views.cart_details, name='cart_details'),
    path('update/<str:product_key>/', views.update_cart, name='update_cart'),
    path('remove/<str:product_key>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear/', views.clear_cart, name='clear_cart'),
    path('checkout/', views.checkout, name='checkout'),
]
