from django.urls import path
from . import views

urlpatterns = [
    path('',views.login, name='login'),
    path('registration/',views.register, name='register'),
    path('refresh/',views.refresh,name='refresh'),
]