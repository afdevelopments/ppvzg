from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('predict/', views.predict, name='predict'),
    path('result/', views.result, name='result'),
]
