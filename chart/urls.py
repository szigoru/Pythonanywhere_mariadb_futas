from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question>/', views.detail, name='detail'),
    path('allrun/', views.allrun, name='allrun'),
    path('stat/', views.stat, name='stat'),
    path('form/', views.form, name='form'),
    path('bevitel/', views.form, name='bevitel'),

]