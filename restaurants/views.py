#encoding=utf-8
from django.shortcuts import render_to_response,render
#from django.views.decorators.csrf import requires_csrf_token
from restaurants.forms import CommentForm

from django.http import HttpResponseRedirect
from restaurants.models import Restaurant, Food, Comment
from django.utils import timezone
from django.template import RequestContext


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
        f = CommentForm()
    return render(request, 'comments.html', locals())


