from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login, name='login'),
    path('logout/',views.logout_view, name='logout-view'),
    path('registration/',views.register, name='register'),
    path('refresh/',views.refresh,name='refresh'),
]