from django.urls import path
from . import views

app_name = 'bvr'

urlpatterns = [
    path('', views.index, name='index'),
    path('users', views.user_list, name='users'),
    path('users/add', views.user_add, name='user-add-form'),
    path('users/update/<user_id>/', views.user_update, name='user-update-form'),

    path('sectors', views.sector_list, name='sectors'),
    path('sectors/add', views.sector_add, name='sector-add-form'),
    path('sectors/update/<sector_id>/', views.sector_update, name='sector-update-form'),

    path('remains', views.remain_list, name='remains'),
    path('remains/add', views.remain_add, name='remains-add-form'),
    path('remains/update/<sector_id>/', views.remain_update, name='remains-update-form'),
]