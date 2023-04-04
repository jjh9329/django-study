from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse,FileResponse
from django.template import loader
from django.core.paginator import Paginator
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView

from json import loads

from .models import Board,Reply

# Create your views here.
# views.py의 함수에 들어있는 request 파라미터 : 요청객체


def index(request):

    print('index() 실행')
    result = None  # 필터링된 리스트
    context = {}
    # request.GET : GET방식으로 보낸 데이터들을 딕셔너리 타입으로 저장
    # print(request.GET)

    # 검색 조건과 검색 키워드가 있어야 필터링 실행
    if 'searchType' in request.GET and 'searchWord' in request.GET:

        search_type = request.GET['searchType']  # GET안의 문자열은
        search_word = request.GET['searchWord']  # HTML의 name속성

        print("search_Type : {},search_word : {}".format(
            search_type, search_word))

        # match : Java의 switch랑 비슷함
        match search_type:
            case 'title':
                result = Board.objects.filter(title__contains=search_word)
            case 'writer':
                result = Board.objects.filter(writer__contains=search_word)
            case 'content':
                result = Board.objects.filter(content__contains=search_word)

        context['searchType'] = search_type
        context['searchWord'] = search_word
    else:  # QueryDict에 검색 조건과 키워드가 없을때
        result = Board.objects.all()
    # board에 id역순으로 정렬
    result = result.order_by('-id')

    # 페이징 넣기
    # Paginaotr(목록,목록에 보여줄 개수)
    paginaotor = Paginator(result, 10)

    # Paginator 클래스를 이용해서 자른 목록의 단위에서
    # 몇번째 단위를 보여줄 것인지 정한다
    page_obj = paginaotor.get_page(request.GET.get('page'))

    # context['board_list'] = result
    context['page_obj'] = page_obj
    return render(request, 'board/index.html', context)


def read(request, id):
    #print(id)
    board = Board.objects.get(id=id)
    #reply_list = Reply.objects.filter(board_obj=id).order_by('-id')
    # board.view_count = board.view_count+1
    board.view_count += 1

    board.save()

    context = {
        'board': board,
        #'replyList' : reply_list
    }
    return render(request, 'board/read.html', context)


def home(request):
    return redirect('/board/')


@login_required(login_url='common:login')
def write(request):
    if request.method == 'GET':
        return render(request, 'board/board_form.html')
    else:
        print(request.POST)
        print(request.FILES)
        title = request.POST['title']
        content = request.POST['content']
        author = request.user  # 요청에 들어있는 User객체
        print(request.user)

        board = Board(
            title=title,
            author=author,
            content=content
        )
        # get 메서드 사용하는 이유
        # 해당하는 키가 없을때 딕셔너리[키]에서 키를 찾으면 ->KeyError
        # 딕셔너리.get("키") -> None
        if request.FILES.get("uploadFile") : # 키가 있다면
            upload_file = request.FILES["uploadFile"]
            #요청에 들어있던 첨부파일을 모델에 설정
            board.attached_file = upload_file
            board.original_file_name = upload_file.name
            print(board.attached_file)
            print(board.original_file_name)

        board.save()
        return redirect('/board/')






        #db에 insert
        # Board.objects.create(
        #     title=title,
        #     author=author,  # user 객체저장
        #     content=content
        # )


        # session_writer = request.session.get('writer')
        # if not session_writer:
        #     session_writer
        #     request.session['writer'] = request.POST['writer']
        # print(session_writer)

        # 객체.save()
        # board.save()  # db에 insert

        # 모델.objects.create(값)


@login_required(login_url='common:login')
def update(request, id):
    board = Board.objects.get(id = id)

    #글쓴이와 현재 접속한 사용자의 username이 다르면 목록으로 리다이렉트해줌
    if board.author.username != request.user.username:
        return HttpResponseRedirect('/board/')

    if request.method == "GET":
        context ={'board' : board }
        return render(request, 'board/update.html', context)

    else:
        board.title = request.POST['board_title']
        board.content = request.POST['board_content']

        #첨부파일이 있다면
        if request.FILES.get('uploadFile'):
            upload_file = request.FILES["uploadFile"]
            #요청에 들어있던 첨부파일을 모델에 설정
            board.attached_file = upload_file
            board.original_file_name = upload_file.name
        else:  #첨부파일이 없다면
            board.attached_file = None
            board.original_file_name = None

        board.save()

    return HttpResponseRedirect('/board/')
    # board = Board.objects.get(id=id)
    # # 글쓴이와 현재 접속한 사용자의 username이 다르면 목록으로 리다이렉트
    # # 유효성 검사

    # if board.author.username != request.user.username:
    #     return redirect('common:login')
    # # 실제 로직이 도는 코드
    # if request.FILES.get('uploadFile'):
    #     upload_file = request.FILES["uploadFile"]
    #     board.attached_file = upload_file
    #     board.original_file_name = upload_file
    # else:
    #     board.attached_file = None
    #     board.original_file_name = None

    #     board.save()
    #     con
    #     return redirect('board:read', board.id)


@login_required(login_url='common:login')
def delete(request, id):
    # 해당객체를 가져옴
    board = Board.objects.get(id=id)
    # 글 작성자의 id 와 접속한 사람의 id 가 다를때
    if board.author.username != request.user.username:
        return redirect('common:login')

    board.delete()
    return redirect('board:index')

def write_reply(request,id):
    print(request.POST)

    user = request.user
    # 요청의 body를 해석
    reply = loads(request.body)

    print(reply)

    reply_text = reply['replyText']
    # Reply.objects.create(
    #     user= user,
    #     reply_content = reply_text,
    #     board_obj = Board.objects.get(id=id)
    # )

    # queryset을 이용해 봅시다
    board = Board.objects.get(id=id)
    board.reply_set.create(
        reply_content = reply_text,
        user= user
    )

    #return HttpResponseRedirect('/board/' + str(id))
    return JsonResponse({'result': 'success'})

def delete_reply(request,id):
    #print(f'id: {id} rid: {rid}')

    #loads(request.body)를 ()로 묶어서 객체로 묶은것(loads(request.body))
    rid = (loads(request.body))["rid"]
    Board.objects.get(id=id).reply_set.get(id =rid).delete()
    #Reply.objects.get(id=rid).delete()
    #return HttpResponseRedirect('/board/' + str(id))
    return JsonResponse({'delete':'success'})

def update_reply(request,id):


    if request.method =='GET':
        rid = request.GET['rid']
        reply= Board.objects.get(id = id).reply_set.get(id=rid)

        context ={
            'id' : reply.id, #id 에 해당하는 Board 객체
            'replyText' : reply.reply_content, #rid에 해당하다는 reply객체
        }

        print("context는 ---------->",context)
        #return render(request, 'board/read.html',context)
        return JsonResponse(context)
    else :
        # JSON 객체로 보냈기 때문에 requset POST로 못 가져온다
        # rid = request.POST['rid']
        #
        print(request.body)
        request_body = loads(request.body)
        rid = request_body["rid"]
        reply_text =request_body["replyText"]
        reply = Board.objects.get(id = id).reply_set.get(id = rid)

        #폼에 들어온 새로운 댓글로 저장
        reply.reply_content =reply_text
        reply.save()
        #return HttpResponseRedirect('/board/' + str(id))
        return JsonResponse({'result':'success'})

def call_ajax(request):
    print('성공했')
    print(request.POST)
    #JSON.stringify 하면 아래 표현은 사용할 수 없음
    # print(request.POST['txt'])

    data = loads(request.body)
    print('템플릿에서 보낸 데이터',data)
    print(data['txt'])
    print(type(data))
    return JsonResponse({'result':'czczczczczczzczccz'})

def load_reply(request,id):
    # id = request.POST['id']
    # print(id)
    # #해당하는 board id 에 달려있는 모든 reply가져오기
    # #1번 방법
    # #Reply.objects.filter(board = id)
    # #2번 방법

    # reply_list=Board.objects.get(id=id).reply_set.all()

    # #QuerySet 그 자체는 js에서 알 수 없는 타입
    # #그래서 JSON타입으로 형변환
    # serialized_list = serializers.serialize("json",reply_list)
    # response = {'response':serialized_list}
    # return JsonResponse(response)

    reply_list = Board.objects.get(id=id).reply_set.all()
    # reply_list의 정보를 가지고 dictionary 만들기
    reply_dict_list = []
    for reply in reply_list:
        reply_dict = {
            'id': reply.id,
            'username':reply.user.username,
            'replyText':reply.reply_content,
            'inputDate':reply.input_date
        }
        reply_dict_list.append(reply_dict)

    context={'replyList':reply_dict_list}

    return JsonResponse(context)



def download(request,id):
    print("글 번호야야양야--------------------->>>>>>",id)
    board = Board.objects.get(id = id)
    attached_file = board.attached_file
    original_file_name = board.original_file_name
    # 글 번호에 달려있떤 첨부파일로 파일형식 응답 객체 생성
    response = FileResponse(attached_file)
    response["Content-Disposition"] = 'attachment; filename=%s' %original_file_name
    return response

### Class Based View ###
class BoardList(ListView):
    # ListView : 목록을 보여주는 기능
    # model = 이 페이지에서 표시할 객체 타입
    # 클래스 기반 뷰에서 사용하는 템플릿은
    # 일반적으로 이름이 객체이름+list.html
    model = Board
    ordering = '-id'
    #ordering 속성에는 문자열로 내가 정렬하고 싶은 열 이름을 쓴다

class BoardDetail(DetailView):
    model = Board
    # template_name 속성 : 내가 별도로 이용하고 싶은 템플릿 파일이 있을때 해당파일 이름 지정
    # template_name을 사용하지 않은면 model이름_detal.html을 찾아간다
    template_name= ' board/read.html'

