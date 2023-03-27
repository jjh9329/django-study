from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
# 장고가 제공하는 기본 회원가입 폼
from django.contrib.auth.forms import UserCreationForm
# Create your views here.


def index(request):
    # 아까 만든 common/index.html을 표시하고
    # localhost:8000/으로 들어갔을때
    # 잘 표시가 되는지 확인
    return render(request, 'common/index.html')


def signup(request):
    if request.method == 'POST':
        # 요청 객체가 담고있는 정보로 사용자 생성 폼 만든다
        print(request.POST)
        form = UserCreationForm(request.POST)

        if form.is_valid():  # from의 내용이 유효하다면
            form.save()  # DB에 폼 정보 저장
            # 폼에 입력한 값 가져오기
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # 사용자 인증
            user = authenticate(username=username, password=raw_password)
            # 로그인
            login(request, user)

            return redirect('/')
    else:
        # GET 방식으로 요청이 오면 비어있는 사용자 생성폼을 만든다
        form = UserCreationForm()
    return render(request, 'common/signup.html', {'form': form})
