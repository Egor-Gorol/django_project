from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('contacts/', views.contact, name='contact'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
]