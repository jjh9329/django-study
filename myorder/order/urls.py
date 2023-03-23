#장고의 기본 라이브러리
from django.urls import path

# 현재 패키지에서 views 를 import 하세요
from . import views

urlpatterns = [
    path('' , views.index),
    
]