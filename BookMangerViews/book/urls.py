from django.conf.urls import url
from django.urls import path

from book import views
from book.views import detail, test4, LoginView, CenterView

app_name = 'book'
urlpatterns = [
    url(r'^test1/$', views.test1),
    path('test2', views.test2, name='test2'),
    # http://127.0.0.1:8000/分类id/书籍id
    # http://127.0.0.1:8000/category_id/boo_id/
    # 分组来获取正则中的数据
    # path(r'^(1)/(100)/$', detail),
    # path(r"^('(\d+)/(\d+)/$", detail),
    # path(r'^(?P<category_id>\d+)/(?P<book_id>\d+)/$)', detail),
    path(r'test3/', views.test3, name='test3'),
    path('test4', views.test4, name='test4'),
    path('test5', views.test5, name='test5'),
    path('test6', views.test6, name='test6'),
    path('test7', views.test7, name='test7'),
    path('test8', views.test8, name='test8'),
    path("set_cookie", views.set_cookie),
    path("get_cookie2", views.get_cookie),
    path("cookie3", views.cookie3, name='cookie3'),

    path('login', LoginView.as_view()),
    path('center', CenterView.as_view()),

    path('index', views.index),
    path('test10',views.test10),

]
