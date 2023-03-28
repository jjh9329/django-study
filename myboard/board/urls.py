# 장고의 기본 라이브러리
from django.urls import path

# 현재 패키지에서 views 를 import 하세요
from . import views

app_name = 'board'
urlpatterns = [
    path('', views.index, name='index'),
    # 해당하는 주소가 입력된다면~
    path('read/<int:id>/', views.read, name='detail'),
    # 수정 주소
    path('<int:id>/update/', views.update, name='update'),
    path('write/', views.write, name='write'),
    # 삭제 주소
    path('<int:id>/delete/', views.delete, name='delete'),
]
