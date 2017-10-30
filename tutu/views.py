from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from . import dbmanager
from . import ArticleInfo


def index(request):
    pageCount = 10
    rows = dbmanager.DBSingleton().queryData("article_tb", 1, 100)
    ArticleList = []
    for item in rows:
        artic = ArticleInfo.Article(item)
        ArticleList.append(artic)

    paginator = Paginator(ArticleList, pageCount)
    page = request.GET.get('page')
    try:
        list = paginator.page(page)
    except PageNotAnInteger:  # 如果页码不是个整数
        list = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        list = paginator.page(paginator.num_pages)  # 取最后一页的记录

    num = len(ArticleList)
    if (num > 5):
        indicator_num = 5
    else:
        indicator_num = num
    numlist = []
    for numItem in range(int(page), int(page) + indicator_num):
        numlist.append(numItem)

    context = {'list': list, 'indicator_num': numlist}
    return render(request, 'tutu/index.html', context)
