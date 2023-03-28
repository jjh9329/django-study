from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
# 장고가 제공하는 기본 회원가입 폼
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.decorators import login_required

# 우리가 만든 커스텀 회원가입 폼
from .forms import UserForm, CustomChangeForm

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


def signup_custom(request):
    if request.method == 'POST':
        print(request.POST)  # QueryDict 한번보기

        # request.POST에 들어있는 정보를 UserForm 형식으로 변환
        form = UserForm(request.POST)

        # Form이 유효한가?
        if form.is_valid():
            form.save()  # 폼의 내용을 DB에 바로저장

            # 폼에 입력한 값 가져오기
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')

            # 사용자 인증후 로그인
            user = authenticate(username=username, password=raw_password,
                                first_name=first_name, last_name=last_name)
            login(request, user)

            return redirect('/')  # 로그인 하고 메인 페이지로 넘김

    else:  # 요청이 GET일때
        form = UserForm()  # 새폼 만들어주기

    return render(request, 'common/signup.html', {'form': form})


@login_required(login_url='common:login')
def delete(request):
    # 비회원일때 가드
    if not request.user.is_authenticated:
        return redirect('common:login')
    # user 정보 삭제
    request.user.delete()
    # render나 redirect의 파라미터로 app_name:url_name작성 가능
    return redirect('common:index', request)


def update(request):
    if request.method == "GET":
        # CustomChangeForminstatnc) 보내면 장고가 제공하는 기본으로 보냄
        form = CustomChangeForm()
        return (request, 'common/update.html', {'form': form})
    else:  # POST
        form = CustomChangeForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('common:index')
    return redirect('common:index')
