from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include

urlpatterns = [
    path('api-token-auth/', obtain_auth_token),
    path('', include(router.urls)),
]
