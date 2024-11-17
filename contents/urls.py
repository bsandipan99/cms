from django.urls import path
from . import views

urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('post/',views.post_content,name='post-content'),
    path('post/<int:pk>/',views.post_detail,name='post-detail'),
    path('post/edit/<int:pk>/',views.post_edit,name='post-edit'),
    path('api/create/',views.create_post,name='create-post'),
    path('<int:pk>/api/read/',views.read_post,name='read-post'),
    path('<int:pk>/api/update/',views.update_post,name='update-post'),
    path('<int:pk>/api/delete/',views.delete_post,name='delete-post'),
]