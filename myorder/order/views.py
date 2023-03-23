from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from .models import Order

# Create your views here.
def index(request):
    
    print('index() 실행')
    order_list = Order.objects.all().order_by('-id')
    
    context = {
        'order_list' : order_list
    }
    
    return render(request, 'order/index.html',context)

def read(request,id):
    print(id)
    order = Order.objects.get(id=id)

    context = {
        'order':order
    }
    return render(request, 'order/read.html', context)

def write(request):
   if request.method == 'GET':
    return render(request,'order/write_form.html')
   else:
    price= request.POST['price']  
    address = request.POST['address']  
    order_text = request.POST['order_text']  

    Order.objects.create(
            price = price,
            address = address, #세션에 있는 값 저장
            order_text = order_text
        )
    
    return HttpResponseRedirect('/order/')
   
def update(request,id):
    order = Order.objects.get(id=id)

    if request.method == 'GET':
      context = {
          'order':order
      }
      return render(request,'order/update.html',context)
    else:
      order.price = request.POST['price']
      order.address= request.POST['address']
      order.order_text= request.POST['order_text']
      
      order.save()
      return HttpResponseRedirect('../../read/'+str(id))

def delete(request,id):
   print(id)
   order = Order.objects.get(id=id)
   if request.method =='GET':
      order.delete()
      return HttpResponseRedirect('/order/')
   

def search_order(request):
    
    search_order = request.POST['searchOrder']
    print(search_order)
    condition = request.POST['condition']

    order_list = []
    if condition == 'all':
        order_list = Order.objects.filter(order_text= search_order)
    else:
        order_list = Order.objects.filter(order_text__contains = search_order)
    context = {
        'order_list' :order_list
    }
    return render(request,'order/index.html',context)
  