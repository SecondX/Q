#encoding=utf-8
from django.shortcuts import render_to_response,render
#from django.views.decorators.csrf import requires_csrf_token
from restaurants.forms import CommentForm
from django.conf import settings
from django.contrib.sessions.models import Session
from django.http import HttpResponseRedirect, HttpResponse, Http404
from restaurants.models import Restaurant, Food, Comment
from django.utils import timezone
from django.template import RequestContext

from django.contrib.auth.decorators import login_required

import logging
def menu(request):
    #path = request.path
    if 'id' in request.GET and len(request.GET['id']) > 0:
        restaurant = Restaurant.objects.get(id=request.GET['id'])
        return render_to_response('menu.html', locals())
    else:
        return HttpResponseRedirect('/restaurants_list/')

from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
class MenuView(DetailView):
    model = Restaurant
    template_name = 'menu.html' #SITE/templates/APPNAME/APP_detail.html
    context_object_name = 'restaurant'
    pk_url_kwarg = 'id' # To fetch urlpattern as its condition to query model

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MenuView, self).dispatch(request,*args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            return super(MenuView, self).get(request, *args, **kwargs)
        except Http404:
            return HttpResponseRedirect('/restaurants_list/')

@login_required
def list_restaurants(request):
    restaurants = Restaurant.objects.all()
    return render_to_response('restaurants_list.html', locals())
from django.views.generic.list import ListView

class RestaurantView(ListView):
    model = Restaurant
    template_name = 'restaurants_list.html' # SITE/template/APPNAME/MODELNAME_list.html
    context_object_name = 'restaurants' # object_list if empty
    #3. change url.py -> url(r'^restaurants_list/$', login_required(restaurants.views.RestaurantsView.as_view()))
    #or override dispatch method by using login_required decorator
    @method_decorator(login_required)
    def dispatch(self,request, *args, **kwargs):
        return super(RestaurantView, self).dispatch(request, *args, **kwargs)
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

from django.views.generic.edit import FormView
class CommentView(FormView):
    form_class = CommentForm
    template_name = 'comments.html'
    success_url = '/comment/'
    initial = {'content':u'我沒意見'}
    def form_valid(self, form):
        Comment.objects.create(
            visitor=form.cleaned_data['visitor'],
            email=form.cleaned_data['email'],
            content=form.cleaned_data['content'],
            date_time=timezone.localtime(timezone.now()),
            restaurant=self.get_object()
            )
        return self.render_to_response(self.get_context_data(
            form=self.form_class(initial=self.initial)))

def set_c(request):
    response = HttpResponse('Set cookie as 8')
    response.set_cookie('number', 8)
    return response
@login_required
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

from django.contrib import auth
# def login(request):
#     if request.user.is_authenticated():
#         return HttpResponseRedirect('/index/')

#     username = request.POST.get('username','')
#     password = request.POST.get('password', '')

#     user = auth.authenticate(username=username, password=password)

#     if user is not None and user.is_active:
#         auth.login(request, user)
#         login_failed = True
#         return HttpResponseRedirect('/index/')
#     return render(request, 'login.html', locals())


def index(request):
    return render(request, 'index.html', locals())

def logout(request):
    auth.logout(request)
    return render(request, 'index.html', locals())


from django.views.generic.base import View, TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'
    def get(self, request, *args, **kwargs):
        '''
        if you don't want to override get method:
            go settings and let 
            TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + ('django.core.context_processors.request',)
            STILL add url('pattern', views.IndexView.as_view())
        '''
        context = self.get_context_data(**kwargs)
        context['request'] = request
        return self.render_to_response(context)
    '''
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        context['time'] = timezone.now()

        return context
    '''