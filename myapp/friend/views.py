from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader

#현재 폴더의 models.py에서 Friend라는 클래스 import
from .models import Friend
# Create your views here.

def index(request):

    context ={}
    t = loader.get_template('friend/index.html')
    return HttpResponse(t.render(context, request))

def add_friend(requset):
    print(requset.method)
    context = {}
    t= loader.get_template('friend/friendForm.html')
    #요청방식이 GET 방식이라면~
    if requset.method == "GET":
        return HttpResponse(t.render(context,requset))
    #요청방식이 POST 방식이라면
    else :
        #요청 객체에서 값을 가져온다
        name = requset.POST['friend_name']
        age = requset.POST['friend_age']
        bigo = requset.POST['friend_bigo']

        print(name,age,bigo)

        f = Friend(
            friend_name = name,
            friend_age = age,
            friend_bigo = bigo,
        )
        f.save()
        # 템플릿 반환 방식(단축) render(요청,템플릿 경로 [,context])
        # return render(request,'friend)

        return HttpResponseRedirect('/friend')

def create_friend(request):
    name = request.POST['friend_name']
    age = request.POST['friend_age']
    bigo = request.POST['friend_bigo']

    Friend.objects.create(
        friend_name = name,
        friend_age = age,
        friend_bigo = bigo
    )

    return HttpResponseRedirect('/friend/')

def show_all(request):
    #DB에 저장된 친구 정보 다 가지고 오기
    fList = Friend.objects.all()
    context = {
        'fList' : fList
    }

    return render(request,'friend/friend_list.html',context)

def search_friend(request):
    search_name = request.POST['searchName']
    condition = request.POST['condition']
    fList = []
    if condition == 'all':
        fList = Friend.objects.filter(friend_name = search_name)
    else:
        fList = Friend.objects.filter(friend_name__contains = search_name)
    context = {
        'fList' :fList
    }
    
    return render(request,'friend/friend_list.html',context)
# path converter(주소로 넘어오는 값)의 이름이 id
def delete_friend(request,id):
    print(id)

    #Friend객체들 중에 파라미터로 넘어온 id와 일치하는
    #id를 가진 객체를 삭제한다
    Friend.objects.get(id=id).delete()
    
    #주소 호출할때 앞에 아무것도 안 붙이면 : 현재 디렉토리에서 이동
    return HttpResponseRedirect('../../show_all/')
    
# def delete_friend2(request,pk):
    
#     delete_name2 = request.GET['id']
#     print("delete_name2>>>>>>>>>>>>",delete_name2)
#     search_name= Friend.objects.get(id = pk)
#     print(search_name)
#     search_name.delete()
    
#     return HttpResponseRedirect('/friend/show_all')
    
def update_friend(request,id):
    print("업데이트 id:",id)
    #파라미터의 id 갑에 해당하는 객체 찾기
    friend = Friend.objects.get(id= id)
    #전송 박식에 따른 화면 표시
    if request.method =='GET':
        # id로 찾은 친구 정보를 템플릿에 표시하기 위해서
        context = {'friend' :friend}
        return render(request,'friend/friend_update.html',context)
    else:
        # id로 찾은 객체에 대해서 폼의 값으로 원래 객체의 값 덮어쓰기
        friend.friend_name = request.POST['friend_name']
        friend.friend_age= request.POST['friend_age']
        friend.friend_bigo= request.POST['friend_bigo']

        friend.save()

        return HttpResponseRedirect("../../show_all/")



