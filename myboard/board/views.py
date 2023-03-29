from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
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
    print(id)
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
        title = request.POST['title']
        content = request.POST['content']
        author = request.user  # 요청에 들어있는 User객체
        print(request.user)

        Board.objects.create(
            title=title,
            author=author,  # user 객체저장
            content=content
        )

        return redirect('/board/')

        # session_writer = request.session.get('writer')
        # if not session_writer:
        #     session_writer
        #     request.session['writer'] = request.POST['writer']
        # print(session_writer)

        # 객체.save()
        # board = Board(
        #     title=title,
        #     writer=writer,
        #     content=content
        # )
        # board.save()  # db에 insert

        # 모델.objects.create(값)


@login_required(login_url='common:login')
def update(request, id):
    board = Board.objects.get(id=id)
    # 글쓴이와 현재 접속한 사용자의 username이 다르면 목록으로 리다이렉트
    # 유효성 검사

    if board.author.username != request.user.username:
        return redirect('common:login')
    # 실제 로직이 도는 코드
    if request.method == 'GET':
        context = {
            'board': board
        }
        return render(request, 'board/update.html', context)
    else:
        board.content = request.POST['board_content']
        board.title = request.POST['board_title']

        board.save()
        return redirect('board:read', board.id)


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
    reply_text = request.POST['replyText']#화면에서 넘어오는 textarea name

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

    return HttpResponseRedirect('/board/' + str(id))

def delete_reply(request,id,rid):
    print(f'id: {id} rid: {rid}')

    Board.objects.get(id=id).reply_set.get(id =rid).delete()
    #Reply.objects.get(id=rid).delete()
    return HttpResponseRedirect('/board/' + str(id))

def update_reply(request,id):

    if request.method =='GET':
        rid = request.GET['rid']
        board= Board.objects.get(id = id)
        context ={
            'update' :'update',
            'board' : board, #id 에 해당하는 Board 객체
            'reply' : board.reply_set.get(id = rid) #rid에 해당하다는 reply객체
        }
    return render(request, 'board/read.html',context)
