from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name = 'home'),
    path('<int:id>/', views.house, name = 'house'),
] 