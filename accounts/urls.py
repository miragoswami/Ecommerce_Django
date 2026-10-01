from django.urls import path

from .views import (
    RegisterView,
    LoginView,
    ProfileView,
    BecomeSellerView,
)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [

    # Register
    path(
        "register/",
        RegisterView.as_view(),
        name="register"
    ),

    # Login
    path(
        "login/",
        LoginView.as_view(),
        name="login"
    ),

    # Refresh JWT
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),

    # Profile
    path(
        "profile/",
        ProfileView.as_view(),
        name="profile"
    ),

    # Become Seller
    path(
        "become-seller/",
        BecomeSellerView.as_view(),
        name="become-seller"
    ),
]