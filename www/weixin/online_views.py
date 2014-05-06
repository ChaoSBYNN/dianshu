# -*- coding:UTF-8 -*-

# created by niuben at 2014-05-01
from django.shortcuts import render_to_response,render,RequestContext
from django.http import StreamingHttpResponse,HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
import simplejson

from api_douban.service import RequestService as RequestService_douban
from models import Article,User

def article_record(request):
    
    return render_to_response('article_record/article_record.html',context_instance=RequestContext(request))

def article_save(request):
    '''
        save article which be sent from article_record page
    '''
    #import time
    #now = time.strftime('%Y-%m-%d %H:%M')
    c={}
    try:
        
        article = Article(title=request.POST.get('title'),author=request.POST.get('author'),\
                    content=request.POST.get('content'))
        article.save()
    
        c = {
             'result':'保存成功！',
             'return_code':0,
        }
    
    except:
        c = {
             'result':'Oops！！！好像出了点差错！点书正在努力反省中~~~',
             'return_code':1,
        }
        
        return render_to_response('article_record/article_save.html',c)

    return render_to_response('article_record/article_save.html',c)

# home page
def online_home_page(request):
    '''
        home web page
    '''
    article_list = Article.objects.all().order_by("-publish_date")[0:10]
    #article_list = Article.objects.raw('select id,title,publish_date from weixin_article limit 10')
    
    for article in article_list:
        article.publish_date = article.publish_date.strftime('%Y年%m月%d日 %H:%M')
    
    
    c = {
         'article_list':article_list,
    }
    
    return render_to_response('online_home_page.html',c,context_instance=RequestContext(request))

def get_article_by_offset(request,offset):
    
    index_start = int(offset) - 1
    index_end = index_start + 10
    
    article_obj = Article.objects.all()
    article_count = article_obj.count()
    article_list = article_obj.order_by("-publish_date")[index_start:index_end]
    #article_list = Article.objects.raw('select id,title,publish_date from weixin_article limit 10')
    
    article_dict = []
    tmp_dict = {}
    
    for article in article_list:
        article.publish_date = article.publish_date.strftime('%Y年%m月%d日 %H:%M')
        tmp_dict = {
                    'id':article.id,
                    'title':article.title,
                    'publish_date':article.publish_date,
                    }
        
        article_dict.append(tmp_dict)
        
    article_json = {
         'article_count':article_count,
         'articles_list':article_dict,
         }
    
    return HttpResponse(simplejson.dumps(article_json))

def get_article_by_id(request,article_id):
    
    article = Article.objects.get(id=article_id)

    c = {
         'title':article.title,
         'publish_date':article.publish_date.strftime('%Y年%m月%d日 %H:%M'),
         'content':article.content,
    }
    
    return HttpResponse(simplejson.dumps(c))


def get_user_count(request):
    '''
        get user count
    '''

    try:    
        user_count = User.objects.all().count()
    except:
        return 9999

    return HttpResponse(user_count)

def details_page(request,book_isbn):
    '''
    details page of news
    '''
    # judge if use mobile device
    #print request.META['HTTP_USER_AGENT']
    
    # get book messages by book id(ISBN)
    rapi = RequestService_douban()
    book_message = rapi.search_book_by_isbn(book_isbn)
    book_id = book_message['id']
    request.session['book_id'] = book_id
    request.session['book_title'] = book_message['title']

    c = {
         # get book_message from douban API
         'tags':book_message['tags'],
         'cover':book_message['images']['large'],
         'title':book_message['title'],
         'author':book_message['author'],
         'publisher':book_message['publisher'],
         'price':book_message['price'],
         'rating':book_message['rating'],
         'author_intro':book_message['author_intro'],
         'summary':book_message['summary'],
         'id':book_message['id'],
         # get book_message from spider
         'rating_details':1,
         }
    
    return render_to_response('online_details_page.html',c,context_instance=RequestContext(request))

def book_gession(request,search_string,is_gession):
    '''
        gession book when type in search box
    '''
    
    book_message_dict = {}
    book_message_json = []
    tmp_dict = {}
    
    book_message_dict = get_books_by_offset(request,search_string=search_string,is_gession=is_gession)
    
    for book_message in book_message_dict['books']:
        
        tmp_dict = {
                    'cover':book_message['images']['small'],
                    'title':book_message['title'],
                    'author':book_message['author'],
                    'publisher':book_message['publisher'],
                    'isbn':str(book_message['isbn13']),
                    }
        
        book_message_json.append(tmp_dict)
    
    return HttpResponse(simplejson.dumps(book_message_json))

def book_search(request):
    '''
        book search page
    '''
    c = {
         'a':'a',
         }
    
    return render_to_response('online_search_page.html',c,context_instance=RequestContext(request))

def search_results(request):
    '''
        search books by offset
    '''
    is_offset = request.GET['is_offset']
    search_string = request.GET['search_string']
    book_message_dict = {}
    book_message_json = []
    tmp_dict = {}
    
    book_message_dict = get_books_by_offset(request,search_string=search_string,is_offset=is_offset)
    
    for book_message in book_message_dict['books']:
        
        tmp_dict = {
                    'cover':book_message['images']['small'],
                    'title':book_message['title'],
                    'author':book_message['author'],
                    'publisher':book_message['publisher'],
                    'pub_date':book_message['pubdate'],
                    'price':book_message['price'],
                    'isbn':str(book_message['isbn13']) if book_message.has_key('isbn13') else book_message['isbn10'],
                    }
        
        book_message_json.append(tmp_dict)
    
    return HttpResponse(simplejson.dumps(book_message_json))
    
def get_books_by_offset(request,search_string='百年孤独',is_offset=0,is_gession=0):
    
    if not int(is_offset):
        request.session['next_offset'] = 0
        if int(is_gession):
            limit = 3
        else:
            limit = 10
    else:
        request.session['next_offset'] += 10
        limit = 10
    
    rapi = RequestService_douban()
    book_message_dict = {}

    book_message_dict = rapi.search_books(unicode(search_string).encode('utf-8'),offset=request.session['next_offset'],limit=limit)
    
    return book_message_dict
    