from django.shortcuts import render
from django.shortcuts import redirect
from dictionary.forms import LoginForm
from dictionary.models import Record
from django.contrib import auth
from django.contrib import messages
from datetime import datetime
from dictionary.dictionary import Dictionary
from django.contrib.auth.decorators import login_required
import re

def __insert_record(request,_keyword):
    r = Record.objects.filter(owner=request.user, keyword=_keyword)
    if len(r) <= 0:
        r = Record()
        r.keyword = _keyword;
        r.owner = request.user;
        r.create_time = datetime.now()
        r.last_lookup_time = datetime.now()
        r.save()
    else:
        robj = r[0]
        robj.last_lookup_time = datetime.now()
        robj.save()

def page_error(request):
    messages.error(request,"Oop!")
    return render(request,'error.html')

@login_required(login_url='login',redirect_field_name='next')
def search(request):
    keyword = request.GET.get("keyword","hello")
    k=re.match(r'[a-zA-Z]{1,16}',keyword)
    if k:
        keyword = k.group(0)
    else:
        messages.error(request,"Invalid request")
        return redirect('index')
    try:
        result = Dictionary.search(keyword)
        if result == None:
            messages.error(request,"No such result")
            return redirect('index')
        image_result =Dictionary.search_image(keyword)
        result['images']=image_result
        if request.user.is_authenticated():
            __insert_record(request,keyword)
        return render(request,'search.html',result)
    except Exception as e:
        messages.error(request,"Unable to retrieve information.")
        return redirect('index')


@login_required(login_url='login',redirect_field_name='next')
def index(request):
    return render(request,'index.html')


def login(request):
    if request.user.is_authenticated():
        return redirect('index')
    if request.method == 'GET':
        form = LoginForm()
        return render(request,'login.html',{'form':form,'next':request.GET.get('next','index')})
    else:
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request,'login.html',{'form':form})
        else:
            cd = form.cleaned_data
            user = auth.authenticate(username=cd['username'],password=cd['password'])
            if user == None or user.is_active == False:
                messages.error(request,"Wrong username or password!");
                return render(request,'login.html',{'form':form})
            else:
                auth.login(request,user)
                if request.POST.get('next','')!='':
                    return redirect(request.POST.get('next',''))
                else:
                    return redirect('index')


def logout(request):
    auth.logout(request)
    return redirect('index')
