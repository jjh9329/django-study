from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from .models import Movie

# Create your views here.
def index(request):
    movie_list = Movie.objects.all()
    result = movie_list
    context = {}
    result = result.order_by('-id')
    paginaotor = Paginator(result, 10)
    page_obj = paginaotor.get_page(request.GET.get('page'))
    context['page_obj'] = page_obj
    return render(request,'exam/index.html',context)

# def reviewOrder(request):
#     result = Movie.objects.all().

def read(request,id):
    movie = Movie.objects.get(id=id)
    context = {
        'movie': movie,
    }
    return render(request, 'exam/read.html', context)

def write(request):
    if request.method == 'GET':
        return render(request, 'exam/movie_form.html')
    else:
        genre = request.POST['genreType']
        movie_name = request.POST['title']
        movie_summary = request.POST['content']

        movie = Movie(
            genre=genre,
            movie_name= movie_name,
            movie_summary=movie_summary
        )
        movie.save()
        return redirect('/')

def update(request, id):
    movie = Movie.objects.get(id = id)

    if request.method == "GET":
        context ={'movie' : movie }
        return render(request, 'exam/update.html', context)

    else:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>수정하기 버튼입니다")
        movie.genre = request.POST['genreType']
        movie.movie_name = request.POST['title']
        movie.movie_summary = request.POST['content']
        movie.save()

    return HttpResponseRedirect('/')

def delete(request, id):
    # 해당객체를 가져옴
    movie = Movie.objects.get(id=id)

    movie.delete()
    return redirect('exam:index')
