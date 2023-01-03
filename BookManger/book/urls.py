from django.urls import path
from django.conf.urls import url

from .views import bookList

urlpatterns = [
    # path('booklist', views.bookList)
    url(r"^booklist/$", bookList)
]
