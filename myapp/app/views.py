from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
# views.py의 함수에 들어있는 request 파라미터 : 요청객체
def index(request):
    template = loader.get_template('app/index.html')

    #dictionary타입의 변수 context
    context = {}

    #response객체안에 템플릿과 표시할값(context),요청(request) 
    return HttpResponse(template.render(context, request))

def call1(request):
    template = loader.get_template('app/template.html')
    print(request)

    context = {}

    return HttpResponse(template.render(context,request))

# REStful 방식으로 호출된 주소에 대한 함수
# 요청 객체 뒤의 파라미터에 해당하는 변수명 써줘야함
def call2(request,number):
    print("number:",number)
    # 파이썬에서는 자료형이 다른 것을 합칠수 없음
    # print("number:"+number)
    template = loader.get_template('app/template.html')

    context = {}

    return HttpResponse(template.render(context,request))

def call3(request):
    #request 객체에서 가져오는 모든 데이터는 str타입
    name = request.GET['name']
    age = request.GET['age']
    print(type(age))
    print("name : ",name)
    print("age : ", age)

    return HttpResponse("호출됨")

def call4(request):
    template = loader.get_template("app/template.html")

    context = {
        # 문자열 하나 보내기
        'item' : 'This text is sent from server',
        'name' : '장재호',
        # 리스트 보내기
        'board_list' : [
          {'title': '1등' ,  'writer':'홍길동'},
          {'title': '2등' , 'writer':'이길동'},
          {'title': '3등' , 'writer':'삼길동'}
        ],
        # 딕셔너리 보내기
        'mydata':{
          'name':'장재호',
          'age' : '20',
          'address':'광주'
        }
    }

    return HttpResponse(template.render(context,request))

def call5(request):
    str_list = ['사과','딸기','바나나']

    template = loader.get_template("app/tag.html")

    context = {
        'list' : str_list,
        'number' : -3
    }

    return HttpResponse(template.render(context,request))

def call6(request):
    template = loader.get_template('app/form.html')
    context = {}

    return HttpResponse(template.render(context,request))
#폼에 입력된 데이터 가져오기
def call_submit(request):
    
    name = request.POST['name']
    age = request.POST['age']

    print('name : ',name)
    print('age : ',age)
    return HttpResponse("submit OK")

def call7(request):
    template = loader.get_template('app/0321.html')

    context ={
        'mydata':{
          'name':'장재호',
          'age':26,
          'josu':'장덕동',
        }
    }

    return HttpResponse(template.render(context,request))
