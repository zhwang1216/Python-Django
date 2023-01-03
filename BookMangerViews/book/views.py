from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse, response
from django.shortcuts import render, redirect
from django.urls import reverse
import json


# Create your views here.
def test1(request):
    return HttpResponse("测试")


def test2(request):
    # 动态路由
    # path = reverse('test1')
    # print(path)
    # 跳转成功页面
    # return redirect('/test1/')
    # return redirect(path)

    # 如果我们设置了namespance，需要通过namespance:name来获取路由
    path = reverse('book:test2')
    print(path)
    return HttpResponse("test2")


def detail(request, category_id, book_id):
    print(category_id, book_id)
    return HttpResponse('details', )


"""
---------------查询字符串-----------------
以？作为一个分隔符
？前边 表示路由
？后边 表示 get方式传递到参数 称之为 查询字符串
？key=value&key=value...
一般情况下都是使用POST方式使用传递。
"""


def test3(request):
    query_params = request.GET
    print(query_params)
    username = query_params['username']
    password = query_params.get('password')
    print(username)
    return HttpResponse("test3")


"""
    JSON request
    {
        'name': 'itcast',
    }
"""


def test4(request):
    print(request.POST)
    body = request.body
    body_str = body.decode()
    print(body)
    print(body_str)
    data = json.loads(body_str)
    print(data)

    return HttpResponse("test4")


def test5(request):
    print(request.META)
    content_type = request.META('CONTENT_TYPE')
    print(content_type)
    print(request.method)
    return HttpResponse("test5")


# "---------HttpResponse-----"
def test6(request):
    data = {'name': 'itcast'}
    # HttpResponse
    # content 传递字符串，不要传递 对象，字典等数据
    # status HTTP status code must be an integer from 100 to 599 只能使用系统规定的
    # content_type 是一个MIME类型
    #               语法 ：大类/小类
    return HttpResponse(data, status=200)


# -----JsonResponse-------
def test7(request):
    data = {'name': 'itcast'}
    return JsonResponse(data)


# ------redirect重定向---
def test8(request):
    # 通过reverse找到路径
    # path = reverse('book:test1')
    # return redirect(path)
    return redirect('https://www.baidu.com/')


"""


    保存在客户端的数据叫做cookie
    1、流程(原理)
        第一次请求过程：
            1、浏览器第一次请求服务器的是，不会携带任何cookie信息
            2、服务器接收到请求之后，发现请求中没有任何cookie信息
            3、服务器设置一个cookie，cookie设置在相应中
            4、浏览器接收到响应之后，返现其中cookie信息，浏览器会将cookie信息保存下来
        第二次：
            5、浏览器第二次及其之后请求都会携带cookie信息
            6、服务器请求之后，会发现cookie信息，就会认识这个请求
    2、看效果
    3、http协议到角度深入账务cookie到流程原理
        第一次：
            1、第一次请求服务器，不会携带任何cookie信息，请求头中没有任何cookie信息
            2、服务器会为响应设置cookie信息，响应头中set_cookie信息
        第二次：
            3、第二次及其以后的请求都会携带cookie信息，请求头中有cookie信息
            4、没有再 在响应头中设置cookie，，响应头中没有set_cookie的信息
            
"""


# 设置cookie
def set_cookie(request):
    response = HttpResponse('ok')
    username = request.GET.get('username')
    response = HttpResponse('cookie1')
    response.set_cookie('username', username)
    # response.set_cookie('itcast1', 'Python')
    # response.set_cookie('itcast2', 'Python2', max_age=360)
    return response


# 读取cookie
def get_cookie(request):
    # cookie1 = request.cookies.get('itcast1')
    # print(cookie1)
    cookies = request.COOKIES
    username = cookies.get('username')

    return HttpResponse("get_cookie_OK")


def cookie3(request):
    response.delete_cookies('itcast1')
    response.delete_cookies('itcast2')
    return HttpResponse("Ok")


"""
    登陆页面
        GET 请求是获取  登陆页面
        POST 请求是验证登陆 （用户名和密码是否正确）
"""


def show_login(request):
    return render(request)


def veri_login(request):
    return redirect('首页')


def login(request):
    if request.method == 'GET':
        # GET请求
        return render(request)
    else:
        # POST请求
        return redirect('首页')


"""
    面向对象
        类视图是采用到面向对象到思路
        1、定义类视图
            1、继承自 View from django.views import View
            2、不同到请求方式 有不同到业务逻辑
                类视图到方法 直接采用http到请求名字，作为函数名 
            3、类视图到方法第二个参数 必须是请求实例对象
                类视图的方法 必须有返回值 返回值是HttpResponse及其子类
"""
from django.views import View


class LoginView(View):
    def get(self):
        return HttpResponse('get')

    def post(self):
        return HttpResponse('POST')


"""
    个人中心页面
    GET 方式 展示 个人中心
    POST 实现个人中心信息的修改
    定义类视图
"""


class CenterView(LoginRequiredMixin, View):
    def get(self, request):
        return HttpResponse('个人中心展示')

    def post(self, request):
        return HttpResponse('个人中心修改')


# -------------模版---------------------------
from datetime import datetime


def index(request):
    # username = request.GET.get('username')
    content = {
        # 'username': username,
        'username': 'zhwang',
        'age': 18,
        'birthday': datetime.now(),
        'friends': ['Tom', 'Jack', 'Rose'],
        'money': {
            '2019': '12k',
            '2020': '15k',
            '2021': '18k',
        },
        'desc': '<script>alert("hot")</script>',

    }
    return render(request, 'book/index.html', context=content)


def test10(request):
    return render(request, 'book/detail.html')

def test11(request):
    # username = request.GET.get('username')
    content = {
        # 'username': username,
        'username': 'zhwang',
        'age': 18,
        'birthday': datetime.now(),
        'friends': ['Tom', 'Jack', 'Rose'],
        'money': {
            '2019': '12k',
            '2020': '15k',
            '2021': '18k',
        },
        'desc': '<script>alert("hot")</script>',

    }
    return render(request, 'Jinja2/index.html', context=content)