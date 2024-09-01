from django.urls import path
from .views import RegisterAPIView, LoginAPIView, SearchUserAPIView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='user_register'),
    path('login/', LoginAPIView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', SearchUserAPIView.as_view(), name='user_search')
]
