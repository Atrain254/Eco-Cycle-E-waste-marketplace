from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # This creates the URL pattern for your marketplace page
    path('', views.item_list, name='item_list'),
    path('add/', views.add_item, name='add_item'),
    path('register/', views.register, name='register'),

    path('login/', auth_views.LoginView.as_view(template_name='marketplace/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('item/<int:pk>/claim/', views.claim_item, name='claim_item'),
]