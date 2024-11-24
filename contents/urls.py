from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('post/',views.dashboard,name='dashboard'),
    path('post/new/',views.post_new,name='post-new'),
    path('post/<int:pk>/',views.post_detail,name='post-detail'),
    path('post/edit/<int:pk>/',views.post_edit,name='post-edit'),
    path('post/api/create/',views.create_post,name='create-post'),
    path('post/api/filter',views.filter_post,name='filter-post'),
    path('post/<int:pk>/api/read/',views.read_post,name='read-post'),
    path('post/<int:pk>/api/update/',views.update_post,name='update-post'),
    path('post/<int:pk>/api/delete/',views.delete_post,name='delete-post'),
]