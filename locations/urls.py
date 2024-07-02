from django.urls import path
from locations import views

urlpatterns=[
    path('map', views.LocationListView.as_view(), name='location-list'),
]
