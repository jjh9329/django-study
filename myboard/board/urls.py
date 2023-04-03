# 장고의 기본 라이브러리
from django.urls import path

# 현재 패키지에서 views 를 import 하세요
from . import views

app_name = 'board'
urlpatterns = [
    path('', views.index, name='index'),
    # 해당하는 주소가 입력된다면~
    path('<int:id>/', views.read, name='read'),
    # 수정 주소
    path('<int:id>/update/', views.update, name='update'),
    path('write/', views.write, name='write'),
    # 삭제 주소
    path('<int:id>/delete/', views.delete, name='delete'),
    path('<int:id>/write_reply/',views.write_reply,name = 'write_reply'),
    #댓글삭제 주소(id: 글번호,rid: 댓글번호)
    #path('<int:id>/delete_reply/<int:rid>/',views.delete_reply,name = 'delete_reply'),
    path('<int:id>/delete_reply/',views.delete_reply,name = 'delete_reply'),
    path('<int:id>/update_reply/',views.update_reply,name='update_reply'),

    #AJAX
    path('callAjax/',views.call_ajax),
    path('<int:id>/load_reply/',views.load_reply, name='load_reply'),

    path('<int:id>/download/',views.download,name = 'download'),
]
