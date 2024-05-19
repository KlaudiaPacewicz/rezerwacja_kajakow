"""
URL configuration for kajaki project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path

from reservations.views import KajakListView, KajakDetailView, confirm_reservation

urlpatterns = [
    path("kajaki/", KajakListView.as_view(), name="kajaki-list"), # 127.0.0.1:8000/kajaki/
    path("kajaki/<int:pk>/<str:start_date>/<str:end_date>", KajakDetailView.as_view(), name="kajak-detail"), # 127.0.0.1:8000/kajaki/[id_kajaku]/
    path("kajaki/<int:kajak_id>/confirm_reservation/", confirm_reservation, name="kajak-confirm-reservation") # 127.0.0.1:8000/kajaki/[id_kajaku]/
]
