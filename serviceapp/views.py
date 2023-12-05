from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import random,os
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from serviceapp.models import UserProfile,WorkerProfile,Review,Service,ServiceCategory,Booking,WorkerProfile1
from .models import Notification
from django.contrib.auth import  authenticate,login,logout
from django.contrib.auth import update_session_auth_hash

def home(request):
    return render(request,'home.html')

def usersignup(request):
    return render(request,'usersignup.html')

def workersignup(request):
    c=ServiceCategory.objects.all()
    return render(request,'workersignup.html',{'c':c})

def login1(request):
    return render(request,'login.html')

def useraction1(request):
    user=request.user.id
    u= UserProfile.objects.get(user_id=user)   
    return render(request,'useraction1.html',{'u':u})

def workeraction1(request):
    user=request.user.id
    w= WorkerProfile.objects.get(user_id=user)  
    return render(request,'workeraction1.html',{'w':w})
 

def dash(request):
    wo=WorkerProfile.objects.all().count()
    us=UserProfile.objects.all().count()
    book=Booking.objects.all().count()
    return render(request,'dashboard.html',{'wo':wo,'us':us,'book':book})



def addcategory(request):
    c=ServiceCategory.objects.all()
    return render(request,'addcategory.html',{'c':c})

def addcategoryworker(request):
    d=ServiceCategory.objects.all()
    return render(request,'addcategoryworker.html',{'d':d})

def useraction(request):
    if request.method == 'POST':
        first_name = request.POST['fname']
        user_name = request.POST['uname']
        last_name = request.POST['lname']
        email_id = request.POST['email']
        contact = request.POST['ph']
        address=request.POST['address']
        image = request.FILES.get('image')
        password=request.POST['password']
        #password = str(random.randint(100000, 999999))
        user_type = request.POST['text']
        if CustomUser.objects.filter(username=user_name).exists():
            messages.info(request, 'This username already exists!!!!!!')
            return redirect('usersignup')
        if CustomUser.objects.filter(email=email_id).exists():
            messages.info(request, 'This Email already exists!!!!!!')
            return redirect('usersignup')
        else:
            user=CustomUser.objects.create_user(first_name=first_name,last_name=last_name,username=user_name,password=password,email=email_id,user_type=user_type)
            user.save()
                
            
            member=UserProfile(address=address,ph=contact,profile_picture=image,user=user)
            member.save()
            messages.info(request, 'You have registered Successfully!!')
            return redirect('/')
    
    return render(request,'usersignup.html')

def workeraction(request):
    error=""
    if request.method == 'POST':
        first_name = request.POST['fname']
        user_name = request.POST['uname']
        last_name = request.POST['lname']
        email_id = request.POST['email']
        address=request.POST['address']
        contact = request.POST['ph']
      
        exp=request.POST['exp']
        agency=request.POST['agency']
        dob=request.POST['dob']
        idtype=request.POST['idtype']
        doc=request.FILES.get('doc')
        cat=request.POST['category']
        #password = str(random.randint(100000, 999999))
        user_type = request.POST['text']
        if CustomUser.objects.filter(username=user_name).exists():
            messages.info(request, 'This username already exists!!!!!!')
            return redirect('workersignup')
        if CustomUser.objects.filter(email=email_id).exists():
            messages.info(request, 'This username already exists!!!!!!')
            return redirect('workersignup')
        else:
            user=CustomUser.objects.create_user(first_name=first_name,last_name=last_name,username=user_name,email=email_id,user_type=user_type)
            user.save()
                
            
            member=WorkerProfile(address= address,phone=contact,agency_name=agency,dob=dob,workexp=exp,typeofid=idtype,idproof=doc,category_id=cat,user=user)
            member.save()
            messages.info(request, 'You have successfully registered')
            return redirect('/')
    return render(request,'workercard.html')


def loginact(request):
    if request.method=='POST':
        user_name=request.POST['uname']
        print(user_name)
        password1=request.POST['password']
        print(password1)
        user=auth.authenticate(username=user_name,password=password1)
       
        
        if user is not None:
            if user.user_type == '1':
                login(request,user)
                return redirect('dash')
            elif user.user_type == '2':
                login(request,user)
                return redirect('useraction1')
            else:
                login(request,user)
                return redirect('workeraction1')
     
            
    messages.error(request,'invalid credentials')
    return render(request,'login.html')
    
def addcat(request):
    cat = request.POST['category']
    c = ServiceCategory(name=cat)
    c.save()
    messages.info(request, 'New Category Added!!!!!!')
    return redirect('addcategory')


def addcatworker(request):
    cat1 = request.POST['category1']
    d = ServiceCategory(name=cat1)
    d.save()
    messages.info(request, 'New Category Added!!!!!!')
    return redirect('addcategoryworker')

def useredit(request,pk):
        u= UserProfile.objects.get(id=pk)
        return render(request,'useredit.html',{'u':u})

def useredit1(request,pk):
    if request.method == 'POST':
        u = UserProfile.objects.get(id=pk)
        v=CustomUser.objects.get(id=u.user_id)
        v.first_name = request.POST['fname']
        v.last_name = request.POST['lname']
        v.email = request.POST['email']
        u.address = request.POST['address']
        u.ph = request.POST['ph']
        if len(request.FILES)!=0:
            if len(u.profile_picture)>0: 
                 os.remove(u.profile_picture.path)
            else:
                 u.profile_picture = request.FILES['image']
            u.profile_picture=request.FILES['image'] 
        
        
        u.save()
        v.save()
        error="no"
        return render(request,'useredit.html',{'u':u,'v':v,'error':error})
        
  
def showuser(request):
    return render(request,'showuser.html')



def workercard(request,pk):
    profile = WorkerProfile.objects.get(id=pk)
    fname = request.user.first_name.capitalize()
    lname=request.user.last_name
    uname=request.user.username
    email=request.user.email
    ph=profile.phone
    address = profile.address
    cat=profile.category.name
    exp=profile.workexp
    
    context = {
        'profile':profile,'fname':fname,'lname':lname,'uname':uname,'email':email,'phone':ph,'address':address,'cat':cat,'exp':exp
        
       
    }
    return render(request,'workercard.html',context)


def workeredit(request,pk):
        e= WorkerProfile.objects.get(id=pk)
        c=ServiceCategory.objects.all()
        return render(request,'workeredit.html',{'e':e,'c':c})

def workeredit1(request,pk):
    if request.method == 'POST':
        e = WorkerProfile.objects.get(id=pk) 
        e.user.first_name = request.POST['fname']
        e.user.last_name = request.POST['lname']
        e.user.user_name=request.POST['uname']
        e.user.email = request.POST['email']
        # e.user.password=request.POST['password']
        e.address = request.POST['address']
        e.phone = request.POST['ph']
        
        e.workexp = request.POST['exp']

        e.category.name=request.POST['cat']

 
        
        
        if len(request.FILES)!=0:
            if len(e.idproof)>0: 
                 os.remove(e.idproof.path)
            else:
                 e.idproof = request.FILES['doc']
            e.idproof=request.FILES['doc'] 
        
        e.save()
        error="no"
        return render(request,'workeredit.html',{'e':e,'error':error})
        
        # return redirect('workeraction1')
    

def showusers(request):
    u = UserProfile.objects.all()
    return render(request,'showusers.html',{'u':u})

def addservice1(request):
    if request.method=='POST':
        title1= request.POST['sername'].capitalize()
        description1 = request.POST['desc']
        cat1 = request.POST['category']
        duration1=request.POST['duration']
        price1 = request.POST['price']
        image1 = request.FILES['serimage']
        p = Service(title=title1,description=description1,price=price1,image=image1,duration=duration1,category_id=cat1)
        p.save()
        messages.info(request, 'New Service has added!!!!')
        return render(request,'addservice.html')
    

def addservice2(request):
    if request.method=='POST':
        title1= request.POST['sername'].capitalize()
        description1 = request.POST['desc']
        cat1 = request.POST['category']
        duration1=request.POST['duration']
        price1 = request.POST['price']
        image1 = request.FILES['serimage']
        p = Service(title=title1,description=description1,price=price1,image=image1,duration=duration1,category_id=cat1)
        p.save()
        messages.info(request, 'New Service has added!!!!')
        return render(request,'addserviceworker.html')
    
def addservice(request):
    c=ServiceCategory.objects.all()
    return render(request,'addservice.html',{'c':c})

def addserviceworker(request):
    c=ServiceCategory.objects.all()
    return render(request,'addserviceworker.html',{'c':c})

def nofitr(request):

    a=Service.objects.all()

    return render(request,'nofitr.html',{'a':a})

def fitr(request,pk):
    ct = Service.objects.filter(category=pk)
    s=ServiceCategory.objects.all()

    return render(request,'fitr.html',{'s':s,'ct':ct})


def bookit(request,pk):
    q = Service.objects.get(id=pk)
    return render(request,'bookingform.html',{'q':q})

def bookit1(request,pk):
   
    if request.method=='POST':
        a=request.POST['day']
        a1=request.POST['address']
        q = Service.objects.get(id=pk)
        u=UserProfile.objects.get(user_id=request.user.id)
        b=Booking(date_booked=a,address=a1,service_id=q.id,customer_id=u.user_id,category_id=q.category_id)
        b.save()
        error="no"
        return render(request,'bookingform.html',{'q':q,'error':error})




def rating(request):
    return render(request,'feedback.html')
    

    
def showworkers(request):
    w = WorkerProfile.objects.all()
    return render(request,'showworkers.html',{'w':w})
    
def showworkersforuser(request):
    w = WorkerProfile.objects.all()
    return render(request,'showworkersforuser.html',{'w':w})

def workercard1(request,pk):
    pro1 = WorkerProfile.objects.get(user=request.user)
    return render(request,'showworkers.html',{'u':pro1})


def deleteworker(request,pk):
    c = WorkerProfile.objects.get(id=pk)
    c.delete()
    return redirect('showworkers')

def deleteuser(request,pk):
    c = UserProfile.objects.get(id=pk)
    c.delete()
    return redirect('showusers')


def logoutt(request):
    logout(request)
    return redirect('home')

def viewservices(request):
    v=Service.objects.all()
    return render(request,'viewservices.html',{'v':v})



def viewworkercards(request):
    cat = ServiceCategory.objects.all()
    w=WorkerProfile.objects.all()

    return render(request,'viewworkercards.html',{'w':w,'cat':cat})

def myorderview(request):
    b=Booking.objects.filter(customer_id=request.user.id,is_approved=True)
    return render(request,'myorderview.html',{'b':b})

def deleteorder(request,pk):
    b = Booking.objects.get(id=pk)
    b.delete()
    return redirect('myorderview')

def approve(request,pk):
    w=WorkerProfile1.objects.get(id=pk)
    a=str(random.randint(100000, 999999))
    use=CustomUser.objects.create_user(email=w.email,username=w.username,password=a,first_name=w.first_name,last_name=w.last_name,user_type='3')
    usr=WorkerProfile(category=w.category,address=w.address,phone=w.phone,workexp=w.workexp,idproof=w.idproof)
    usr.user=use
    usr.save()
    w.delete()
    subject='Admin Approved'
    message = f'Hello {usr.user.username},\nYour username: {usr.user.username}\nPassword: {a}'
    recipient=use.email
    send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient])
    return render(request,'dashboard.html',locals())

def approdetails(request):
    s=Notification.objects.all()
    let=WorkerProfile1.objects.all()
    return render(request,'approvaltable.html',{'use':let},{'s':s})

def disapproval(request,pk):
    pre=WorkerProfile1.objects.get(id=pk)
    pre.delete()
    return redirect('show_notification')

def workeractionfake(request):
    error=""
    if request.method == 'POST':
        first_name = request.POST['fname']
        user_name = request.POST['uname']
        last_name = request.POST['lname']
        email_id = request.POST['email']
        address=request.POST['address']
        contact = request.POST['ph']
        exp=request.POST['exp']
        doc=request.FILES.get('doc')
        cat=request.POST['category']
    
        if CustomUser.objects.filter(username=user_name).exists():
            messages.info(request, 'This username already exists!!!!!!')
            return redirect('workersignup')
  
        else:
             member1=WorkerProfile1(first_name=first_name,last_name=last_name,username=user_name,email=email_id,address= address,phone=contact,workexp=exp,idproof=doc,category_id=cat)
             member1.save()
             messages.info(request, 'Please wait for admin approval for successful registration!')
        return redirect('workersignup')
    


def show_notification(request):
    s=WorkerProfile1.objects.all()
    return render(request,'approvaltable.html',{'s':s})

def logoutt(request):
    logout(request)
    return redirect('home')

def servicebooking(request):
    s=Booking.objects.filter(is_approved=False)
   
    return render(request,'viewservices.html',{'s':s})


def completefunction(request):
    com=Booking.objects.filter(is_approved=False)
    return render(request,'viewservices.html',{'com':com})

def disapprovalorder(request,pk):
    pre=Booking.objects.get(id=pk)
    pre.delete()
    return redirect('servicebooking')

def approvalorder(request,pk):
    w=Booking.objects.get(id=pk)
    w.is_approved=True
    c=WorkerProfile.objects.get(user_id=request.user.id)
    w.worker_id=c.id
    w.save()
    return redirect('servicebooking')







def update_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        if request.user.check_password(current_password):
            
            if new_password == confirm_new_password:
                
                request.user.set_password(new_password)
                request.user.save()

                update_session_auth_hash(request, request.user)

                messages.success(request, 'Your password was successfully updated!')
                return redirect('update_password')
            else:
                messages.error(request, 'New password and confirm new password do not match.')
        else:
            messages.error(request, 'Incorrect current password.')

    return render(request, 'changepassword.html')

def usercard(request,pk):
    userprofile = UserProfile.objects.get(id=pk)
    fname = request.user.first_name.capitalize()
    lname=request.user.last_name
    uname=request.user.username
    email=request.user.email
    ph=userprofile.ph
    address = userprofile.address
    image=userprofile.profile_picture
    
    context = {
        'userprofile':userprofile,'fname':fname,'lname':lname,'uname':uname,'email':email,'ph':ph,'address':address,'image':image
        
       
    }
    return render(request,'usercard.html',context)


def viewallbookings(request):

        bo = Booking.objects.filter(is_approved=True)
        return render(request,'viewallbookings.html',{'bo':bo})


def viewprodadminandworker(request):

    a=Service.objects.all()

    return render(request,'viewprodadminandworker.html',{'a':a})

def feedback(request,pk):
    q = Service.objects.get(id=pk)   
    return render(request,'feedback.html',{'q':q})


def rating(request,pk):
    if request.method=='POST':
        r=request.POST['rating']
        c=request.POST['comment']
        q = Service.objects.get(id=pk)
        u=UserProfile.objects.get(user_id=request.user.id)
        b=Booking(rating=r,comment=c,service_id=q.id,customer_id=u.user_id)
        b.save()
        error="no"
        return render(request,'useraction1.html',{'q':q,'error':error})

        

