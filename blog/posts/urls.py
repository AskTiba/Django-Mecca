from django.urls import path
from . import views

urlpatterns = [
    # path('home/', views.home, name = 'home'),
    path("", views.home, name="home"),
    path("/quotes", views.quotes, name="quotes"),
    # path('<int:id>/', views.house, name = 'house'),
    path("<str:character_id>/", views.character_detail, name="character_detail"),
] 