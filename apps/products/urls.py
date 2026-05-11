from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('search/', views.product_search, name='search'),
    path('<slug:slug>/', views.category_list, name='category'),
    path('<slug:slug>/detail/', views.product_detail, name='detail'),
    path('<slug:slug>/quick-view/', views.quick_view, name='quick_view'),
]
