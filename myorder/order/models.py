from django.db import models
from django.utils import timezone 
# Create your models here.
# class Board(models.Model):
#     #번호는 pk 설정 안하면 장고가 자동으로 id 부여해줌
#     ### 필드와 필드 사이에 컴마 금지
#     title = models.CharField(max_length=100) # 제목
#     content = models.TextField(null=False,blank=False) # 내용
#     writer = models.CharField(max_length=10) #글쓴이
#     input_date = models.DateTimeField(default=timezone.now) #작성시간
#     view_count = models.IntegerField(default=0) #조회수
class Order(models.Model):
    order_date = models.DateTimeField(default=timezone.now)
    order_text = models.TextField(null=False,blank=False)
    price = models.IntegerField(default=0)
    address = models.TextField(null=False,blank=False)