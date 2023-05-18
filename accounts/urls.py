from django.urls import path, include
from .views import UserRegistrationView,  CustomTokenObtainPairView,ProfileView,BuyCreditView


urlpatterns = [
    #resgistration
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    #login
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),   
    #profile
    path('profile/', ProfileView.as_view(), name='profile'),
    #buy credit
    path('buy_credit/', BuyCreditView.as_view(), name='buy-credit'),
]
