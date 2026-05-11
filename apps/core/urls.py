from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('orders/', views.orders_page, name='orders'),
    path('contact/', views.contact, name='contact'),
]
