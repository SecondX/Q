#encoding=utf-8
from django.shortcuts import render_to_response,render
#from django.views.decorators.csrf import requires_csrf_token
from restaurants.forms import CommentForm

from django.contrib.sessions.models import Session
from django.http import HttpResponseRedirect, HttpResponse
from restaurants.models import Restaurant, Food, Comment
from django.utils import timezone
from django.template import RequestContext

import logging
def menu(request):
    #path = request.path
    if 'id' in request.GET and len(request.GET['id']) > 0:
        restaurant = Restaurant.objects.get(id=request.GET['id'])
        return render_to_response('menu.html', locals())
    else:
        return HttpResponseRedirect('/restaurants_list/')
def list_restaurants(request):
    restaurants = Restaurant.objects.all()
    return render_to_response('restaurants_list.html', locals())

#@requires_csrf_token
def comment(request, request_id):

    if request_id:
        r = Restaurant.objects.get(id=request_id)
    else:
        return HttpResponseRedirect('/restaurants_list/')
    if request.POST:
        visitor = request.POST['visitor']
        content = request.POST['content']
        email = request.POST['email']
        date_time = timezone.localtime(timezone.now())
        Comment.objects.create(visitor=visitor, content=content, email=email, date_time=date_time, restaurant=r)
        visitor, email, content = ('','','')
        form = CommentForm()
    return render(request, 'comments.html', locals())


def set_c(request):
    response = HttpResponse('Set cookie as 8')
    response.set_cookie('number', 8)
    return response

def get_c(request):
    if 'number' in request.COOKIES:
        return HttpResponse('got a number {}'.format(request.COOKIES['number']))
    else:
        return HttpResponse('No Cookie')

def session_test(request):
    if not request.session.session_key:
        request.session.save()
    sid = request.session.session_key
    s = Session.objects.get(pk=sid)
    s_info = 'Session ID:{0}<br>Expire Date:{1}<br>Data:{2}'.format(sid, str(s.expire_date), str(s.get_decoded()))
    # s_info = 'session ID:'+sid
    return HttpResponse(s_info)

