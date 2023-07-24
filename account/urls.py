from django.urls import path
from .import views
from django.contrib.auth import views as auth_view


urlpatterns = [
    path('',views.index,name="home"),
    path('register/',views.register, name="register"),
    path('registration/otp/',views.otpVerification, name="otp-Registration"),
    path('login/',views.userLogin, name="user-login"),
    path('login/otp/',views.otpLogin, name="otp-login"),
    path('logout/',auth_view.LogoutView.as_view(template_name='logout.html')),
 
    
]
