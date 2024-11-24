from django.contrib import admin
from django.urls import path, include
import users.urls
import contents.urls
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token-refresh'),
    path('users/', include(users.urls)),
    path('', include(contents.urls)),
]
