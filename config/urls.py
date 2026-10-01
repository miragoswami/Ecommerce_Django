
from django.contrib import admin
from django.urls import path  , include #path() is used to create a URL route.
from accounts.views import RegisterView


from rest_framework_simplejwt.views import (
    TokenObtainPairView, #handles login return usrename+ password and return jwt tokens
    TokenRefreshView,
)
# JWT means JSON Web Token.
# JWT is commonly used to keep users logged in when your frontend and backend communicate through APIs.

# TokenRefreshView
# This is used when the access token expires.
# Instead of asking the user to log in again, the refresh token can be used to get a new access token.
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/' , include('accounts.urls')),
    path('api/' , include('products.urls')),

    path('api/' , include('cart.urls')),
    path('api/' , include('wishlist.urls')),

    path('api/' , include('orders.urls')),
    path('api/' , include('payments.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)