from django.contrib import admin
# Register your models here.
from .models import Note,reply
# Register your models here.
# 내가 만든 커스텀 모델 등록
admin.site.register(Note)
admin.site.register(reply)