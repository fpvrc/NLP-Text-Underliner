from django.urls import path, re_path

from . import views



urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('pages/<int:reading_id>/', views.pages, name='drag_and_drop_upload'),
    #path('pages/', views.pages, name='drag_and_drop_upload'),
    path('clear/', views.clear_database, name='clear_database'),
    path('logout', views.logout, name='logout'),
    path('upload', views.upload, name='upload'),
]