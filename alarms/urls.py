from django.urls import path
from alarms import views

urlpatterns=[
    path('option/', views.OptionView.as_view(), name='option'),
    path('create/',views.AlarmContentView.as_view(),name='message-create'),
]