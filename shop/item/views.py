from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import I

# Create your views here.
def index(request):
    i_list = I.objects.all()
    context = {
        'iList' : i_list
    }
    return render(request,'item/index.html',context)

def write(request):
    if request.method == 'GET':
        return render(request, 'item/i_form.html/')
    else:
        print(request.POST)
        item_code = request.POST['item_code']
        item_name = request.POST['item_name']
        item_count = request.POST['item_count'] # 요청에 들어있는 User객체
        print(request.user)

        i= I(
            item_code=item_code,
            item_count=item_count,
            item_name=item_name
        )
        # get 메서드 사용하는 이유
        # 해당하는 키가 없을때 딕셔너리[키]에서 키를 찾으면 ->KeyError
        # 딕셔너리.get("키") -> None
        i.save()
        return redirect('/')

def read(request,id):
    item = I.objects.get(id=id)
    context = {
        'item': item,
    }
    return render(request, 'item/read.html', context)

def update(request,id):
    item = I.objects.get(id=id)
    if request.method == "GET":
        context ={'item' : item }
        return render(request, 'item/update.html', context)
    else:
        item.item_code = request.POST['item_code']
        item.item_name = request.POST['item_name']
        item.item_count = request.POST['item_count']
        item.save()

    return HttpResponseRedirect('/')


def delete(request,id):
    item = I.objects.get(id=id)
    item.delete()
    return redirect('item:index')