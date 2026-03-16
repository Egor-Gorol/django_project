from django import urls
from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('history/', views.order_history, name='order_history'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('detail/<int:order_id>/', views.order_detail, name='order_detail'),
]