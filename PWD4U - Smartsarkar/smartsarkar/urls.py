"""smartsarkar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from smartapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.homepage),
    path('contact',views.contact),
    path('login/',views.login),
    path('registrationpublic',views.registrationpublic),
    path('registrationauthority',views.registrationauthority),
    path('homeadmin',views.homeadmin),
    path('homepublic',views.homepublic),
    path('homeauthority',views.homeauthority),
    path('complaint',views.complaint),
    path('feedback',views.feedback),
    path('adminviewcomplaints',views.adminviewcomplaints),
    path('adminviewfeedbacks',views.adminviewfeedbacks),
    path('authorityviewcomplaints',views.authorityviewcomplaints),
    path('authorityaddresponse',views.authorityaddresponse),
    path('adminviewauthority',views.adminviewauthority),
    path('allocation',views.allocation),
    path('viewuser',views.viewuser),
    path('deleteuser', views.deleteuser),
    path('deleteauthority', views.deleteauthority),
    path('approveauthority',views.approveauthority),
    path('viewauthorities',views.viewauthorities),
    path('deletecomplaint',views.deletecomplaint),
    path('addrating',views.addrating),
    path('viewrating',views.viewrating),
    path('averagerating',views.averagerating),
    path('userviewrating',views.userviewrating),
    path('userviewavgrating',views.userviewavgrating),
    path('viewlocation',views.viewlocation),
    path('viewlocation1',views.viewlocation1),
    path('userpro',views.userpro),
    path('updateuserpro',views.updateuserpro),
    path('satisfied',views.satisfied),
    path('unsatisfied',views.unsatisfied),


    


]
