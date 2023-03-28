from django.urls import path
from django.contrib.auth import views as auth_view

# 현재폴더에서 views.py를 가지고 오는데 그이름이 c_v
from . import views as common_view

app_name = 'common'

urlpatterns = [
    path('', common_view.index, name='index'),
    path('login/', auth_view.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(), name='logout'),
    # path('signup/', common_view.signup),
    # 회원가입
    path('signup/', common_view.signup_custom, name='signup'),
    # 회원 삭제
    # path('delete/', common_view.delete(), name='delete'),
    # path('update/', common_view.update, name='update')
]
