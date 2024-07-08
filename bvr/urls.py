from django.urls import path
from . import views

app_name = 'bvr'

urlpatterns = [
    path('users', views.user_list, name='users'),
    path('remains', views.remain_list, name='remains'),
    path('sectors', views.sector_list, name='sectors'),
]