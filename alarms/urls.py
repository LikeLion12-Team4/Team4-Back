from django.urls import path
from alarms import views

urlpatterns=[
    path('', views.AlarmSetView.as_view(), name='option'),
    path('<int:user_id>/', views.OptionView.as_view(), name='option'),
    path('message/<int:user_id>/', views.AlarmView.as_view(), name='option'),
    path('content/', views.contentcreate, name='contentcreate'),
] 
