from django.urls import path
from . import views

urlpatterns = [
    # path('home/', views.home, name = 'home'),
    path("", views.home, name="home"),
    path("/quotes", views.quotes, name="quotes"),
    path('/play', views.play, name = 'play'),
    path('/flex', views.flex, name = 'flex'),
    path('/grid', views.grid, name = 'grid'),
    path("<str:character_id>/", views.character_detail, name="character_detail"),
] 