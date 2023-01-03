from django.http import HttpResponse
from django.shortcuts import render


# 定义视图：提供书籍列表信息
def bookList(request):
    return HttpResponse('OK!')
