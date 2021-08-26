from django.urls import path

from authentication.views import user, new_token_view

urlpatterns = [
    path('register/', user.UserSignUp.as_view(), name='register'),
    path('login/', user.UserLogin.as_view(), name='login'),
    path('token/new-auth-token/', new_token_view.RegenerateAuthToken.as_view(),
         name='new-auth-token'),
]
