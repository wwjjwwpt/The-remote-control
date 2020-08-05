"""ftp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from sample import views
from django.conf.urls import url


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^folder/(?P<url>.+)/$', views.show_folder),
    url(r'^problem/(?P<pid>.+)/$', views.index),
    url(r'^$', views.munue),
    url(r'^readf',views.gettxt),
    url(r'^mkdirf',views.mkdir),
    url(r'^mkfile',views.mkfile),
    url(r'^deletef',views.delete),
    url(r'^putcode',views.puttxt),
    url(r'^runjar',views.runjar),
    url(r'^endjar',views.endjar),
    url(r'^makejar',views.makejar),
    url(r'^makedata',views.makemysql),
    url(r'^enddata',views.stopmysql),
    path('accounts/', include('registration.backends.default.urls')),
    path('login/', views.login),
    path('logout/', views.logout),
    path('userinfo/', views.userinfo),
    path('addport/',views.addport)
]

