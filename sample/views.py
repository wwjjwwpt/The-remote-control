from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib import auth
from json import loads,dumps
from django.contrib.auth.decorators import login_required
import os
from .models import PathItem,FileItem
from django.views.decorators.csrf import csrf_exempt
import shutil
from django.contrib.auth.models import User
from . import models

import requests
from . import  forms

def login(request):
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            login_name=request.POST['username'].strip()
            login_password=request.POST['password']
            user = authenticate(username=login_name, password=login_password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    print("success")
                    messages.add_message(request, messages.SUCCESS, '成功登录了')
                    return redirect('/')
                else:
                    messages.add_message(request, messages.WARNING, '账号尚未启用')
            else:
                messages.add_message(request, messages.WARNING, '登录失败')
        else:
            messages.add_message(request, messages.INFO,'请检查输入的字段内容')
    else:
        login_form = forms.LoginForm()
    return render(request, 'login.html', locals())

def munue(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    context_dic = {}
    context_dic['username'] = username
    context_dic['problem'] = [{"pid":"1", "sid":"实验一","title":"javaspringboot入门"},{"pid":"2","sid":"实验二", "title":"javaspring连接mysql"}]
    return render(request, 'mune.html', context_dic)

def index(request,pid):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        return HttpResponse('请登录')
    a = [{"pid": "1", "sid": "实验一", "title": "javaspringboot入门","detail":"入门springboot并且在123路由下输出index\n数据库账号:root\n数据库密码：123456\n端口:127.0.0.1:3307"},
                              {"pid": "2", "sid": "实验二", "title": "javaspring连接mysql","detail":"连接数据库并且读取向数据库中插入数据并且读取\n数据库账号:root\n数据库密码：123456\n端口:127.0.0.1:3307"}]
    current1 = '/Users/wenjiawei/django/spring/myapp'
    current = '/Users/wenjiawei/django/spring/'+ username
    if not os.path.exists(current):
        command = 'sudo cp -r ' + current1 + ' ' + current
        a = os.system(command)
        print(a)
    context_dic = {}
    print(int(pid)-1)
    context_dic['pdetail'] = a[int(pid)-1]
    context_dic['current'] = current
    ps = os.listdir(current)
    path = []
    file = []
    for n in ps:
        if (n == '.DS_Store'):
            continue
        v = os.path.join(current, n)
        if os.path.isdir(v):
            p = PathItem(n, '',True)
            print(p.url)
            path.append(p)
        else:
            f = FileItem(n, '')
            file.append(f)

    context_dic['path'] = path
    context_dic['file'] = file
    context_dic['parentu'] = '/'
    print(context_dic)
    return render(request, 'index1.html', context_dic)


def show_folder(request, url):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        return HttpResponse('请登录')
    current = '/Users/wenjiawei/django/spring/'+username+'/'+url
    context_dic = {}
    context_dic['current'] = current
    ps = os.listdir(current)
    print(ps)
    path = []
    File = []
    for n in ps:
        if (n == '.DS_Store'):
            continue
        v = os.path.join(current, n)
        if os.path.isdir(v):
            p = PathItem(n, url,True)
            path.append(p)
        else:
            f = FileItem(n, url)
            File.append(f)
    # context_dic['parent'] = os.path.pardir(url)
    context_dic['path'] = path
    context_dic['file'] = File
    print(url)
    if(url.rfind('/')!=-1):
        context_dic['parent'] = '/folder/'+url[0:url.rfind('/')]
        context_dic['parentu'] = '/'+url
        print('=====')
        print(context_dic['parentu'])
    else:
        context_dic['parent'] = '/problem/'+'1'
        context_dic['parentu'] = '/'+url
        print('------')
        print(context_dic['parentu'])
    return render(request, 'index1.html', context_dic)

@csrf_exempt
def gettxt(request):
    if (request.method == 'POST'):
        postBody = request.body
        json_result = loads(postBody)
    if request.user.is_authenticated:
        username = request.user.username
    else:
        return HttpResponse('请登录')
    current = '/Users/wenjiawei/django/spring/'+username+'/'+json_result['url']
    print(current)
    with open(current, 'r') as f:
        r = f.readlines()
    str = ''
    for i in r:
        str += i
    return HttpResponse(str)

@csrf_exempt
def puttxt(request):
    if (request.method == 'POST'):
        postBody = request.body
        json_result = loads(postBody)
    if request.user.is_authenticated:
        username = request.user.username
    else:
        return HttpResponse('请登录')
    current = '/Users/wenjiawei/django/spring/'+username+'/'+json_result['url']
    print(current)
    print(json_result['content'])
    f= open(current, 'w')
    f.write(json_result['content'])
    return HttpResponse('succeess')

@csrf_exempt
def mkdir(request):
    if (request.method == 'POST'):
        postBody = request.body
        json_result = loads(postBody)
    if request.user.is_authenticated:
        username = request.user.username
    else:
        return HttpResponse('请登录')
    print("++++++j")
    print(json_result['fname'],json_result['froot'])
    current = '/Users/wenjiawei/django/spring/'+username + json_result['froot']+'/'+json_result['fname']
    path = current.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        os.makedirs(path)
        print(path + ' 创建成功')
        return HttpResponse('success')
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return HttpResponse('False')

@csrf_exempt
def delete(request):
    if (request.method == 'POST'):
        postBody = request.body
        json_result = loads(postBody)
    if request.user.is_authenticated:
        username = request.user.username
    else:
        return HttpResponse('请登录')
    print(json_result['froot'])
    current = '/Users/wenjiawei/django/spring/'+username+'/'+ json_result['froot']
    path = current.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if  isExists:
        # 如果不存在则创建目录
        shutil.rmtree(path)
        print(path + ' 删除成功')
        return HttpResponse('success')
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return HttpResponse('False')

@csrf_exempt
def mkfile(request):
    if (request.method == 'POST'):
        postBody = request.body
        json_result = loads(postBody)
    if request.user.is_authenticated:
        username = request.user.username
    else:
        return HttpResponse('请登录')
    print(json_result['fname'],json_result['froot'])
    current = '/Users/wenjiawei/django/spring/'+username+'/' + json_result['froot']+json_result['fname']
    print(current)
    path = current.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        fd = open(path, mode="w", encoding="utf-8")
        fd.close()
        print(path + ' 创建成功')
        return HttpResponse('success')
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return HttpResponse('False')

@csrf_exempt
def runjar(request):
    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
        fuport = models.Springports.objects.filter(user=user)
        if(len(fuport)==0):
            return HttpResponse('无端口去个人信息中生成端口')
    else:
        return HttpResponse('请登录')
    command ='cp /Users/wenjiawei/django/spring/'+username+'/target/first-app-by-maven-1.0.0-SNAPSHOT.jar /home/ubuntu/exp/1;sudo docker build -t first-app1-'+username+' /home/ubuntu/exp/1;sudo docker run -d -p '+str(fuport[0].port)+':8080 first-app1'
    try:
        os.system(command)
        return HttpResponse('running')
    except:
        return HttpResponse('error')

@csrf_exempt
def endjar(request):
    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
        fuport = models.Springports.objects.filter(user=user)
        if(len(fuport)==0):
            return HttpResponse('无端口去个人信息中生成端口')
    else:
        return HttpResponse('请登录')
    command = 'sudo docker ps -q --filter ancestor="first-app1-"'+username+' | xargs -r sudo docker stop;sudo docker ps -a | grep "Exited" |xargs sudo docker rm;sudo docker images|grep first-app1|xargs sudo docker rmi'
    try:
        os.system(command)
        return HttpResponse('running')
    except:
        return HttpResponse('error')

@csrf_exempt
def makejar(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        return HttpResponse('请登录')
    os.chdir('/Users/wenjiawei/django/spring/'+username)
    command ='/usr/local/apache-maven-3.6.3/bin/mvn package'
    try:
        a = os.system(command)
        print(a)
        return HttpResponse(a)
    except:
        return HttpResponse('error')

@csrf_exempt
def makemysql(request):
    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
        fumport = models.Mysqlports.objects.filter(user=user)
        if(len(fumport)==0):
            return HttpResponse('无端口去个人信息中生成端口')
    else:
        return HttpResponse('请登录')
    command = 'sudo docker run -p '+str(fumport[0].port)+'3307:3306 --name mysql1'+username+' -v $PWD/conf:/etc/mysql/conf.d -v $PWD/logs:/logs -v $PWD/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.7.26'
    try:
        a = os.system(command)
        print(a)
        return HttpResponse(a)
    except:
        return HttpResponse('error')

@csrf_exempt
def stopmysql(request):
    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
        fumport = models.Mysqlports.objects.filter(user=user)
        if(len(fumport)==0):
            return HttpResponse('无端口去个人信息中生成端口')
    else:
        return HttpResponse('请登录')
    command = 'sudo docker stop  `sudo docker ps -aq --filter name=mysql1'+username+'`;sudo docker rm    `sudo docker ps -aq --filter name=mysql1`'
    try:
        a = os.system(command)
        print(a)
        return HttpResponse(a)
    except:
        return HttpResponse('error')

def logout(request):
    auth.logout(request)
    messages.add_message(request, messages.INFO, "成功注销了")
    return redirect('/')

@login_required(login_url='/login/')
def userinfo(request):
    userinfo = {}
    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
        print(type(username))
        fuport = models.Springports.objects.filter(user=user)
        fumport = models.Mysqlports.objects.filter(user=user)
        if (len(fuport) == 0):
            port = 'no'
        else:
            port = 'yes'
            sport = fuport[0].port
            mport = fumport[0].port
        try:
            user = User.objects.get(username=username)
            print(user)
            userinfo = models.Springport.objects.filter(user=user)
        except:
            fail = 'fail'
    return render(request, 'userinfo.html', locals())

def addport(request):
    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
        print(user)
        fuport = models.Springports.objects.filter(user = user)
        fmport = models.Mysqlports.objects.filter(user=user)
        print(fuport)
        if(len(fuport)==0 and len(fmport)==0):
            print("不存在添加端口")
            models.Springports.objects.create(user = user)
            models.Mysqlports.objects.create(user=user)
        else:
            print("已存在不添加")
        return HttpResponse('suceess')


