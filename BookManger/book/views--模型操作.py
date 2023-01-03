from django.db.models import Model, F, Q, Sum
from django.http import HttpResponse
from django.shortcuts import render


# 定义视图：提供书籍列表信息
def bookList(request):
    return HttpResponse('OK!')


from models import BookInfo, PeopleInfo

# ----------增加数据---------
# save：通过创建模型类对象，执行对象的save()方法保存到数据库中。
book = BookInfo(
    name='python入门',
    pub_date='2010-1-1'
)
book.save()
# create
# 通过模型类.objects.create()保存。
PeopleInfo.objects.create(
    name='itheima',
    book=book
)

# ---------修改数据--------------
# save() 修改模型类对象的属性，然后执行save()方法
person = PeopleInfo.objects.get(name='itheima')
person.name = 'itcast'
person.save()
# update:使用模型类.objects.filter().update()，会返回受影响的行数
PeopleInfo.objects.filter(name='itheima').update(name='传播智客')

# ----------删除数据--------------
# 模型类对象delete
person = PeopleInfo.objects.get(name='传播智客')
person.delete()
# 模型类.objects.filter().delete()
BookInfo.objects.filter(name='传播智客').delete()

# ------------基本操作-----------
# get得到某个数据,get查询单一结果，如果不存在会抛出模型类.DoesNotExist异常。
BookInfo.objects.get(id=1)
BookInfo.objects.get(pk=2)
try:
    book = BookInfo.objects.get(id=20)
except BookInfo.DoesNotExist as e:
    print(e)
# all获取所有数据
BookInfo.objects.all()
# count 统计数据
BookInfo.objects.count()

# ------过滤查询-----
# ----filter,get,exclude----
"""
    select * from bookInfo where 条件语句
    相当于 :
    filter:筛选/过滤 返回n个结果
    get:返回一个结果
    exclude:排除符合条件剩余的结果,相当于not
    语法形式:
        filter(字段名_运算符=值)为例
"""

# 查询编号为1的图书
# exact:表示判等
BookInfo.objects.filter(id_exact=1)
# 简写为
BookInfo.objects.filter(id=1)

# 查询书名包含'湖'的图书
# 模糊查询：contains:是否包含
BookInfo.objects.filter(name__contains='传')
# 查询书名以'部'结尾的图书
# startswith,endswith:以指定开头或结尾的
BookInfo.objects.filter(name__endswith='部')
# 以上运算符都区分大小写，在这些运算符前加上i表示不区分大小写，如iexact、icontains、istartswith、iendswith.

# 查询书名为空的图书
# 空查询：isnull:是否null
BookInfo.objects.filter(name__isnull=True)

# 查询编号为1或3或5的图书
# 范围查询:in 是否在包含范围内
BookInfo.objects.filter(id__in=[1, 3, 5])

# 查询编号大于3的图书
"""
    比较查询：
        1、gt 大于(greater then)
        2、gte 大雨等于(greater then equal)
        3、lt 小于(less then)
        4、lte 小雨等于(less then equal)
"""
BookInfo.objects.filter(id_gt=3)

# 查询1980年发表的图书
# 日期查询 year、month、day、week_day、hour、minute、second：对日期时间类型的属性进行运算。
BookInfo.objects.filter(pub_date__year=1980)
# 查询1990年1月1日后发表的图书
BookInfo.objects.filter(pub_date__gt='1990-1-1')

# ------F语法------
"""
    F对象的语法格式：
        filter(字段名__运算符=F('字段名'))
"""
from django.db.models import F

# 查询阅读量大于等于评论量的图书。
BookInfo.objects.filter(readcount__gt=F('commentcount'))
# 查询阅读量大于2倍评论量的图书。
BookInfo.objects.filter(readcount__gt=F('commentcount') * 2)

# ----------Q对象---------
"""
    Q对象可以使用&、|连接，&表示逻辑与，|表示逻辑或。
    Q对象前可以使用~操作符，表示非not。
"""
# 查询阅读量大于20，并且编号小于3的图书。
from django.db.models import Q

BookInfo.objects.filter(readcount__gt=20, id__lt=3)
# 或者
BookInfo.objects.filter(readcount__gt=20).filter(id__lt=3)
# 查询阅读量大于20的图书，改写为Q对象如下
BookInfo.objects.filter(Q(readcount__gt=20))
# 查询阅读量大于20，或编号小于3的图书，只能使用Q对象实现
BookInfo.objects.filter(Q(readcount__gt=20) | Q(id__lt=3))
# 查询编号不等于3的图书。
BookInfo.objects.filter(~Q(id=3))

# --------聚合函数---------
"""
    使用aggregate()过滤器调用聚合函数。聚合函数包括：Avg平均，Count数量，Max最大，Min最小，Sum求和
"""
# 查询图书的总阅读量。
BookInfo.objects.aggregate(Sum('readcount'))
# 使用count时一般不使用aggregate()过滤器。
BookInfo.objects.count()

# --------排序函数---------
# # 默认升序
BookInfo.objects.all().order_by('readcount')
# 降序
BookInfo.objects.all().order_by('-readcount')

# ---------关联函数----------
# 查询书籍为1的所有人物信息
# 一对多查询
book = BookInfo.objects.get(id=1)
book.peopleinfo_set.all()

# 多对一查询
person = PeopleInfo.objects.get(id=1)
person.book
# 多对应的模型类对象.关联类属性_id
person = PeopleInfo.objects.get(id=1)
person.book_id

"""
    关联过滤查询：
        由多模型类条件查询一模型类数据
    语法：
        关联模型类名小写__属性名__条件运算符 = 值
    注意：
        如果没有"__运算符"部分，表示等于。
"""

# 查询图书，要求图书人物为"郭靖"
book = BookInfo.objects.filter(peopleinfo__name='郭靖')
print(book)
# 查询图书，要求图书中人物的描述包含"八"
book = BookInfo.objects.filter(peopleinfo__description__contains='八')

"""
    关联过滤查询：
        由一模型类条件查询多模型类数据:
    语法：
        一模型类关联属性名__一模型类属性名__条件运算符=值
    注意：
        如果没有"__运算符"部分，表示等于。
"""
# 查询书名为“天龙八部”的所有人物
peopleInfo = PeopleInfo.objects.filter(book__name='天龙八部')
# 查询图书阅读量大于30的所有人物
peopleInfo = PeopleInfo.objects.filter(book__readcount__gt=30)

# ------查询集QuerySet-----
"""
    Django的ORM中存在查询集的概念。
        查询集，也称查询结果集、QuerySet，表示从数据库中获取的对象集合。
    all()：返回所有数据。
    filter()：返回满足条件的数据。
    exclude()：返回满足条件之外的数据。
    order_by()：对结果进行排序。
    1、惰性执行
    2、缓存
    3、限制查询集
       注意：不支持负数索引。


"""
books = BookInfo.objects.filter(readcount__gt=30).order_by('pub_date')
# 1、惰性执行
books = BookInfo.objects.all()
for book in books:
    print(book.name)

# 2、缓存
# 使用同一个查询集，第一次使用时会发生数据库的查询，然后Django会把结果缓存下来，再次使用这个查询集时会使用缓存的数据，减少了数据库的查询次数。

# 限制查询集
# 查询集进行切片后返回一个新的查询集，不会立即执行查询。
# 如果获取一个对象，直接使用[0]，等同于[0:1].get()，但是如果没有数据，[0]引发IndexError异常，[0:1].get()如果没有数据引发DoesNotExist异常。
# 获取第1、2项，运行查看。

books = BookInfo.objects.all()[0:2]

# ------分页查询-----
#查询数据
books = BookInfo.objects.all()
#导入分页类
from django.core.paginator import Paginator
#创建分页实例
paginator=Paginator(books,2)
#获取指定页码的数据
page_skus = paginator.page(1)
#获取分页数据
total_page=paginator.num_pages