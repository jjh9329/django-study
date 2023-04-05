from django.urls import path
from . import views
app_name = 'exam'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/', views.read, name='read'),
    path('write/', views.write, name='write'),
    path('<int:id>/update/',views.update, name='update'),
    path('<int:id>/delete/',views.delete, name='delete'),
]