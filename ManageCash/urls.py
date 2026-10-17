from django.contrib import admin
from django.urls import path
from ManageCash import views


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Home
    path('', views.dashboard, name='home'),

    # Registration and Login
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Cash Management
    path('addcash/', views.addcash, name='addcash'),
    path('addexpense/', views.addexpense, name='addexpense'),

    # Change Password
    path('change-password/', views.change_pass, name='change_pass'),
    
]