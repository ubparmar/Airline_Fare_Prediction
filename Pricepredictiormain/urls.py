from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import profile_edit_view
urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.predict_price, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),
    path('accounts/profile/', views.profile, name='profile'), 
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('result/<str:prediction>/', views.show_prediction, name='show_prediction'),
]
