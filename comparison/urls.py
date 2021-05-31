from django.urls import path
from . import views

urlpatterns = [
    path('',views.comparison,name='comparison'),
    path('signup',views.signup,name='signup'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout')
]