"""
URL configuration for secure_auth project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path
from .views import (
    login_view,
    DocumentListView,
    DocumentCreateView,
    DocumentUpdateView,
    DocumentDeleteView,
    DocumentPublishView
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('documents/', DocumentListView.as_view(), name='document_list'),
    path('documents/create/', DocumentCreateView.as_view(), name='document_create'),
    path('documents/<int:pk>/edit/', DocumentUpdateView.as_view(), name='document_edit'),
    path('documents/<int:pk>/delete/', DocumentDeleteView.as_view(), name='document_delete'),
    path('documents/<int:pk>/publish/', DocumentPublishView.as_view(), name='document_publish'),
]
