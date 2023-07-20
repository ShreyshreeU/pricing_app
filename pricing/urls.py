from django.urls import path
from . import views

app_name = 'pricing'

urlpatterns = [
    path('configurations/', views.pricing_configuration_list, name='configuration_list'),
    path('configurations/add/', views.add_pricing_configuration, name='add_configuration'),
    path('calculate-price/', views.calculate_price, name='calculate_price'),
]
