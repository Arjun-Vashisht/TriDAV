from django.urls import path
from . import views

app_name = 'seo'

urlpatterns = [
    path('robots.txt', views.robots_txt, name='robots'),
    path('bedsheet-exporter-india/', views.seo_landing, {'slug': 'bedsheet-exporter-india'}, name='bedsheet_exporter'),
    path('hotel-towel-supplier/', views.seo_landing, {'slug': 'hotel-towel-supplier'}, name='hotel_towel'),
    path('bulk-comforter-manufacturer/', views.seo_landing, {'slug': 'bulk-comforter-manufacturer'}, name='bulk_comforter'),
    path('kitchen-towel-supplier/', views.seo_landing, {'slug': 'kitchen-towel-supplier'}, name='kitchen_towel'),
    path('seo/<slug:slug>/', views.seo_landing, name='landing'),
]
