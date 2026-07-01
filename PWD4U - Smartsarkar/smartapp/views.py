from django.shortcuts import render,redirect
from .models import Public,Authority,Complaint,Feedback,Allocation,Rating
from django.contrib import messages
from django.db.models import Avg
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Create your views here.

def homepage(request):
    return render(request,"homepage.html")
def contact(request):
    return render(request,"contact.html")
def registrationpublic(request):
    if request.POST:
        name=request.POST['name']
        address=request.POST['address']
        aanum=request.POST['aanum']

        phone=request.POST['phone']
        email=request.POST['email']
        password=request.POST['password']
        # image=request.FILES['image']
        User_exist=User.objects.filter(username=email).exists()
        if not User_exist:
            try:
               pass
               
            except Exception as e:
                messages.info(request,e)
                print(e)
            else:
                try:
                    u=User.objects.create_user(username=email,password=password,is_staff=0,is_active=1)
                    u.save()
                    r=Public.objects.create(name=name,address=address,phone=phone,email=email,user=u,aanum=aanum)
                    r.save()
                except Exception as e:
                    messages.info(request,e)
                    print(e)
                else:
                    messages.info(request,"Registration successfull")
        else:
            messages.info(request,"email already registered")
   
    return render(request,"registrationpublic.html")

def registrationauthority(request):

    if request.POST:
        name=request.POST['name']
        official=request.POST['official']
        address=request.POST['address']
        phone=request.POST['phone']
        email=request.POST['email']
        password=request.POST['password']
        image=request.FILES['image']
        User_exist=User.objects.filter(username=email).exists()
        if not User_exist:
            try:
               pass
                # r=Registration.objects.create(name=name,address=address,phone=phone,email=email,image=image)
                # r.save()
            except Exception as e:
                messages.info(request,e)
                print(e)
            else:
                try:
                    u=User.objects.create_user(username=email,password=password,is_staff=1,is_active=0)
                    u.save()
                    r=Authority.objects.create(authorityname=name,official=official,address=address,phone=phone,email=email,proof=image,user=u)
                    r.save()
                except Exception as e:
                    messages.info(request,e)
                    print(e)
                else:
                    messages.info(request,"Registration successfull")
        else:
            messages.info(request,"email already registered")
   
    return render(request,"registrationauthority.html")

def login(request):
    if(request.POST):
        email=request.POST['username']
        password=request.POST['password']

        user=authenticate(username=email,password=password)
        print(user)
        if user is not None:
            userdata=User.objects.get(username=email)
            if userdata.is_superuser==1:
                return redirect("/homeadmin")
            elif userdata.is_staff==0:
                request.session["email"]=email
                d=Public.objects.get(email=email)
                request.session['pid']=d.id
                request.session["name"]=d.name
                return redirect("/homepublic")
            elif userdata.is_staff==1:
                request.session["email"]=email
                e=Authority.objects.get(email=email)
                request.session['aid']=e.id
                request.session["name"]=e.authorityname
                return redirect("/homeauthority")
            
    return render(request,"login.html")

def homeadmin(request):
    return render(request,"homeadmin.html")

def homepublic(request):
    return render(request,"homepublic.html")

def homeauthority(request):
    return render(request,"homeauthority.html")

def complaint(request):
    pid = request.session['pid']
    # aid=request.session['aid']
    cust = Public.objects.get(id=pid)
    # auth=Authority.objects.get(id=aid)
    # msg=""
    if request.POST:
        complaint = request.POST['complaint']
        desc= request.POST['desc']
        image=request.FILES['image']
        lat = request.POST['l1']
        lon = request.POST['l2']
        authority=request.POST['att']
        comp = Complaint.objects.create(pid=cust,complaint=complaint,desc=desc,proof=image,status="Pending",lat=lat,lon=lon,authority=authority)
        comp.save()
        messages.info(request,"Complaint submitted")
    data=Complaint.objects.filter(pid=pid)
    return render(request, "complaint.html",{"data":data})

def feedback(request):
    pid = request.session['pid']
    # aid=request.session['aid']
    cust = Public.objects.get(id=pid)
    # auth=Authority.objects.get(id=aid)
    # msg=""
    if request.POST:
        feedback = request.POST['desc']
        feed = Feedback.objects.create(pid=cust,Feedback=feedback)
        feed.save()
        messages.info(request,"Feedback Submited")
    data = Feedback.objects.all()
    return render(request, "feedback.html",{"data":data})

def adminviewcomplaints(request):
    data=Complaint.objects.all()
    return render(request,"adminviewcomplaints.html",{"data":data})

def adminviewfeedbacks(request):
    data=Feedback.objects.all()
    return render(request,"adminviewfeedbacks.html",{"data":data})

def authorityviewcomplaints(request):
    aid=request.session['aid']
    aaid=Authority.objects.get(id=aid)
    data=Complaint.objects.filter(aid=aaid)
    # data=Complaint.objects.all()
    return render(request,"authorityviewcomplaints.html",{"data":data})

def authorityaddresponse(request):
    id=request.GET.get("id")
    if request.POST:
        response=request.POST['response']
        Complaint.objects.filter(id=id).update(rply=response,status="Submitted")
        messages.info(request,"Response added")
    return render(request,"authorityaddresponse.html")

def adminviewauthority(request):
    data=Authority.objects.all()
    return render(request,"adminviewauthority.html",{"data":data})

def allocation(request):
    id=request.GET.get("id")
    at=Authority.objects.all()
    data=Complaint.objects.get(id=id)
    if request.POST:
        att=request.POST['att']
        duedt=request.POST['duedt']
        aut=Authority.objects.get(id=att)
        s=Allocation.objects.create(compid=data,authid=aut)
        s.save()
        data.aid=aut
        data.status="Alloted"
        data.duedt=duedt
        data.save()
        messages.info(request,"Allocated successfully")
        return redirect("/adminviewcomplaints")
    return render(request,"allocation.html",{"data":data,"at":at})

def viewuser(request):
    data=Public.objects.all()
    return render(request,"viewuser.html",{"data":data})

def deleteuser(request):
    id=request.GET.get("id")
    email=request.GET.get("email")
    Public.objects.filter(id=id).delete()
    User.objects.filter(username=email).delete()
    return redirect("/viewuser")
def deleteauthority(request):
    id=request.GET.get("id")
    email=request.GET.get("email")
    Authority.objects.filter(id=id).delete()
    User.objects.filter(username=email).delete()
    return redirect("/viewauthorities")

def viewauthorities(request):
    User_inactive=Authority.objects.filter(user__is_active=0)
    User_active=Authority.objects.filter(user__is_active=1)
    return render(request, "viewauthorities.html", {"data": User_inactive, "data1": User_active})
    
def approveauthority(request):
    id=request.GET.get("id")
    User_active=User.objects.filter(id=id).update(is_active=1)
    return redirect("/viewauthorities")

def deletecomplaint(request):
    id=request.GET.get("id")
    Complaint.objects.filter(id=id).delete()
    return redirect("/adminviewcomplaints")

def addrating(request):
    id = request.GET.get("id")
    auth=Authority.objects.get(id=id)
    pid=request.session['pid']
    cust=Public.objects.get(id=pid)
    if request.POST:
        rating =  request.POST['rating']
        s = Rating.objects.create(pid=cust,aid=auth,rating=rating)
        s.save()
        messages.info(request,"Successfully Added")
    return render(request,'addrating.html')

def viewrating(request):
    data=Rating.objects.all()
    return render(request,"viewrating.html",{"data":data})

def userviewrating(request):
    data=Rating.objects.all()
    return render(request,"userviewrating.html",{"data":data})

def averagerating(request):
    id=request.GET.get("id")
    data=Authority.objects.get(id=id)
    rate=Rating.objects.filter(aid=id).aggregate(avg1=Avg('rating'))
    d=rate['avg1']
    return render(request,"averagerating.html",{"data":data,"d":d})

def userviewavgrating(request):
    id=request.GET.get("id")
    data=Authority.objects.get(id=id)
    rate=Rating.objects.filter(aid=id).aggregate(avg1=Avg('rating'))
    d=rate['avg1']
    return render(request,"userviewavgrating.html",{"data":data,"d":d})

def viewlocation(request):
    id=request.GET.get('id')
    req=Complaint.objects.get(id=id)
    return render(request,'viewlocation.html',{'lat':req.lat,'lng':req.lon})

def viewlocation1(request):
    id=request.GET.get('id')
    req=Complaint.objects.get(id=id)
    return render(request,'viewlocation1.html',{'lat':req.lat,'lng':req.lon})

def userpro(request):
    uid=request.session['pid']
    data=Public.objects.get(id=uid)
    return render(request,"userpro.html",{"data":data})

def updateuserpro(request):
    id=request.GET.get("id")
    data=Public.objects.get(id=id)  
    if request.POST:
        name=request.POST['name']
        address=request.POST['address']
        phone=request.POST['phone']
        Public.objects.filter(id=id).update(name=name,address=address,phone=phone)
        messages.info(request,"Updation successfull")
        return redirect("/userpro")

    return render(request,"updateuserpro.html",{"data":data})

def satisfied(request):
    id=request.GET.get("id")
    c = Complaint.objects.get(id=id)
    c.status = 'Completed'
    c.save()
    return redirect("/complaint")

def unsatisfied(request):
    id=request.GET.get("id")
    c = Complaint.objects.get(id=id)
    if request.POST:
        desc = request.POST['desc']
        c.addinfo = desc
        c.status = 'Not Satisfied'
        c.save()
        messages.info(request,"Added Successfully")
        return redirect("/complaint")
    return render(request,"unsatisfied.html")
    



