from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from .models import Board

# Create your views here.
# views.py의 함수에 들어있는 request 파라미터 : 요청객체
def index(request):
    
    print('index() 실행')
    board_list = Board.objects.all().order_by('-id')
    
    context = {
        'board_list' : board_list
    }
    
    return render(request, 'board/index.html', context)

def read(request,id):
    print(id)
    board = Board.objects.get(id=id)


    #board.view_count = board.view_count+1
    board.view_count += 1

    board.save()

    context = {
        'board':board
    }
    return render(request, 'board/read.html', context)

def home(request):
   return HttpResponseRedirect('/board/')

def write(request):
   if request.method == 'GET':
    return render(request,'board/board_form.html')
   else:
    title = request.POST['title']  
    content = request.POST['content']  

    session_writer = request.session.get('writer')
    if not session_writer:
       request.session['writer'] =request.POST['writer']  #session_writer 
    print(session_writer)


    #객체.save()
    # board = Board(
    #    title = title,
    #    writer= writer,
    #    content= content
    # )
    # board.save() #db에 insert

    #모델.objects.create(값)
    Board.objects.create(
            title = title,
            writer = request.session.get('writer'), #세션에 있는 값 저장
            content = content
        )
    
    return HttpResponseRedirect('/board/')

def update(request,id):
    board = Board.objects.get(id=id)

    if request.method == 'GET':
      context = {
          'board':board
      }
      return render(request,'board/update.html',context)
    else:
      board.title = request.POST['board_title']
      board.content= request.POST['board_content']
      board.writer= request.POST['board_writer']
      
      board.save()
      return HttpResponseRedirect('../../read/'+str(id))

def delete(request,id):
   print(id)
   board = Board.objects.get(id=id)
   if request.method =='GET':
      board.delete()
      return HttpResponseRedirect('/board/')
   