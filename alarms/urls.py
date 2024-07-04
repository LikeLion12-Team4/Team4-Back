from django.urls import path
from alarms import views

urlpatterns=[
    path('', views.AlarmSetView.as_view(), name='alarm-set'),
    path('option/', views.OptionView.as_view(), name='option'),
    path('message/', views.MessageView.as_view(), name='alarm'),
    
] 
