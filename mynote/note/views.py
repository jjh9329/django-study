from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.template import loader
from django.core.paginator import Paginator
from django.core import serializers
from django.contrib.auth.decorators import login_required

from json import loads

from .models import Note,Reply

# Create your views here.
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
                result = Note.objects.filter(title__contains=search_word)
            case 'writer':
                result = Note.objects.filter(writer__contains=search_word)
            case 'content':
                result = Note.objects.filter(content__contains=search_word)

        context['searchType'] = search_type
        context['searchWord'] = search_word
    else:  # QueryDict에 검색 조건과 키워드가 없을때
        result = Note.objects.all()
    # note에 id역순으로 정렬
    result = result.order_by('-id')

    # 페이징 넣기
    # Paginaotr(목록,목록에 보여줄 개수)
    paginaotor = Paginator(result, 10)

    # Paginator 클래스를 이용해서 자른 목록의 단위에서
    # 몇번째 단위를 보여줄 것인지 정한다
    page_obj = paginaotor.get_page(request.GET.get('page'))

    # context['note_list'] = result
    context['page_obj'] = page_obj
    return render(request, 'note/index.html', context)


def read(request, id):
    #print(id)
    note = Note.objects.get(id=id)
    #reply_list = Reply.objects.filter(note_obj=id).order_by('-id')
    # note.view_count = note.view_count+1
    note.view_count += 1

    note.save()

    context = {
        'Note': Note,
        #'replyList' : reply_list
    }
    return render(request, 'note/read.html', context)


def home(request):
    return redirect('/note/')


@login_required(login_url='common:login')
def write(request):
    if request.method == 'GET':
        return render(request, 'note/note_form.html')
    else:
        title = request.POST['title']
        content = request.POST['content']
        author = request.user  # 요청에 들어있는 User객체
        print(request.user)

        Note.objects.create(
            title=title,
            author=author,  # user 객체저장
            content=content
        )

        return redirect('/note/')



@login_required(login_url='common:login')
def update(request, id):
    note = Note.objects.get(id=id)
    # 글쓴이와 현재 접속한 사용자의 username이 다르면 목록으로 리다이렉트
    # 유효성 검사

    if note.author.username != request.user.username:
        return redirect('common:login')
    # 실제 로직이 도는 코드
    if request.method == 'GET':
        context = {
            'note': note
        }
        return render(request, 'note/update.html', context)
    else:
        note.content = request.POST['note_content']
        note.title = request.POST['note_title']

        note.save()
        return redirect('note:read', note.id)


@login_required(login_url='common:login')
def delete(request, id):
    # 해당객체를 가져옴
    note = Note.objects.get(id=id)
    # 글 작성자의 id 와 접속한 사람의 id 가 다를때
    if note.author.username != request.user.username:
        return redirect('common:login')

    note.delete()
    return redirect('note:index')

def write_reply(request,id):
    print(request.POST)

    user = request.user
    reply_text = request.POST['replyText']  #화면에서 넘어오는 textarea name

    # queryset을 이용해 봅시다
    note = Note.objects.get(id=id)
    note.reply_set.create(
        reply_content = reply_text,
        user= user
    )

    return HttpResponseRedirect('/note/' + str(id))

def delete_reply(request,id,rid):
    print(f'id: {id} rid: {rid}')

    Note.objects.get(id=id).reply_set.get(id =rid).delete()
    #Reply.objects.get(id=rid).delete()
    return HttpResponseRedirect('/note/' + str(id))

def update_reply(request,id):


    if request.method =='GET':
        rid = request.GET['rid']
        note= Note.objects.get(id = id)
        context ={
            'update' :'update',
            'note' : note, #id 에 해당하는 note 객체
            'reply' : note.reply_set.get(id = rid) #rid에 해당하다는 reply객체
        }
        return render(request, 'note/read.html',context)
    else :
        rid = request.POST['rid']
        print("id :",rid)
        print(">>>>>>>>>>>>>>>>>>>>>>댓글수정누름")
        reply = Note.objects.get(id = id).reply_set.get(id = rid)
        #폼에 들어온 새로운 댓글로 저장
        reply.reply_content = request.POST['replyText']
        reply.save()
        return HttpResponseRedirect('/note/' + str(id))

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

def load_reply(request):
    id = request.POST['id']
    print(id)
    #해당하는 note id 에 달려있는 모든 reply가져오기
    #1번 방법
    #Reply.objects.filter(note = id)
    #2번 방법

    reply_list=Note.objects.get(id=id).reply_set.all()

    #QuerySet 그 자체는 js에서 알 수 없는 타입
    #그래서 JSON타입으로 형변환
    serialized_list = serializers.serialize("json",reply_list)
    response = {'response':serialized_list}
    return JsonResponse(response)