from django.urls import path

from . import views

urlpatterns = [
    path('', views.Editor.as_view(), name='editor'),
    path('<int:document_id>/', views.Document.as_view(), name='document'),
]
