from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Main page
    path('get_mapping_data/', views.get_mapping_data, name='get_mapping_data'),  # Endpoint for JSON data
    path('process_input/', views.process_input, name='process_input'),  # Endpoint to handle form submission of main cricket game
    path('play_super_over/', views.play_super_over, name='play_super_over'), #Endpoint to handle form submission of main Super Over
    path('super_over/', views.super_over_view, name='super_over'), #Endpoint of form for super over
]
