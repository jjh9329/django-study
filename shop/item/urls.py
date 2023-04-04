from django.urls import path

# 현재 패키지에서 views 를 import 하세요
from . import views

app_name = 'item'
urlpatterns = [
    path('',views.index,name='index'),
    path('<int:id>/',views.read,name = 'read'),
    path('<int:id>/update',views.update,name = 'update'),
    path('<int:id>/delete',views.delete,name = 'delete'),
    path('write/', views.write, name='write'),
]