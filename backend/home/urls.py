from django.urls import path

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('<invalid_path>/', views.InvalidPath.as_view(), name='invalid_path')
]
