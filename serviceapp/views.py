from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from django.conf import settings
from django.core.mail import send_mail
import random,os
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required,user_passes_test
from serviceapp.models import UserProfile,WorkerProfile,Review,Service,ServiceCategory,Booking,WorkerProfile1,NewCategoryRequest
from .models import Notification
from django.contrib.auth import  authenticate,login,logout
from django.contrib.auth import update_session_auth_hash
from django.core.files.storage import FileSystemStorage
from functools import wraps

def home(request):
    return render(request,'home.html')

def usersignup(request):
    return render(request,'usersignup.html')

def workersignup(request):
    c=ServiceCategory.objects.all()
    return render(request,'workersignup.html',{'c':c})

def login1(request):
    return render(request,'login.html')

# def useraction1(request):
#     user=request.user.id
#     u= UserProfile.objects.get(user_id=user)   
#     a=Service.objects.all()

#     return render(request,'useraction1.html',{'u':u,'a':a})


# def useraction1(request):
#     user = request.user.id
#     u = UserProfile.objects.get(user_id=user)
#     categories = Service.objects.values('category__name').distinct()
#     services_by_category = {category['category__name']: Service.objects.filter(category__name=category['category__name']) for category in categories}

#     return render(request, 'usercategoryhome.html', {'u': u, 'services_by_category': services_by_category})

@login_required(login_url='loginact')
def useraction1(request):
    user = request.user.id
    u = UserProfile.objects.get(user_id=user)
    categories = ServiceCategory.objects.all()

    return render(request, 'useraction1.html', {'u': u, 'categories': categories})

@login_required(login_url='loginact')
def usercategory(request, category_id):
    user = request.user.id
    u = UserProfile.objects.get(user_id=user)
    category = get_object_or_404(ServiceCategory, pk=category_id)
    services = Service.objects.filter(category=category)

    return render(request, 'usercategory.html', {'u': u, 'category': category, 'services': services})


# def workeraction1(request):
#     user=request.user.id
#     w= WorkerProfile.objects.get(user_id=user)  
#     ab=Booking.objects.filter(is_approved=0).count()
#     return render(request,'workeraction1.html',{'ab':ab,'w':w})

@login_required(login_url='loginact')
def workeraction1(request):
    user = request.user.id
    w = WorkerProfile.objects.get(user_id=user)  
    ab = Booking.objects.filter(approval_status='pending', service__worker=w, is_approved=0).count()
    
    return render(request, 'workeraction1.html', {'ab': ab, 'w': w})

@login_required(login_url='loginact')
def dash(request):
    wo=WorkerProfile.objects.all().count()
    us=UserProfile.objects.all().count()
    book=Booking.objects.all().count()
    ab1=WorkerProfile1.objects.all().count()
    return render(request,'dashboard.html',{'wo':wo,'us':us,'book':book,'ab1':ab1})


@login_required(login_url='loginact') 
def addcategory(request):
    c=ServiceCategory.objects.all()
    return render(request,'addcategory.html',{'c':c})

@login_required(login_url='loginact')
def view_categories(request):
    categories = ServiceCategory.objects.all()
    return render(request, 'viewcategoryonaddcategory.html', {'categories': categories})

@login_required(login_url='loginact')
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
            messages.info(request, 'This username already exists!')
            return redirect('usersignup')
        if CustomUser.objects.filter(email=email_id).exists():
            messages.info(request, 'This Email already exists!')
            return redirect('usersignup')
        else:
            # Use a non-standard autocomplete value for the username field
            user=CustomUser.objects.create_user(first_name=first_name,last_name=last_name,username=user_name,password=password,email=email_id,user_type=user_type)
            user.save()
            member=UserProfile(address=address,ph=contact,profile_picture=image,user=user)
            member.save()
            messages.info(request, 'Registration Success. Please Login!')
            return redirect('usersignup')
    
    return render(request,'usersignup.html')

@login_required(login_url='loginact')
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
        cert=request.FILES.get('document')
        #password = str(random.randint(100000, 999999))
        user_type = request.POST['text']
        if CustomUser.objects.filter(username=user_name).exists():
            messages.info(request, 'This username already exists!')
            return redirect('workersignup')
        if CustomUser.objects.filter(email=email_id).exists():
            messages.info(request, 'This email-id already exists!')
            return redirect('workersignup')
        else:
            user=CustomUser.objects.create_user(first_name=first_name,last_name=last_name,username=user_name,email=email_id,user_type=user_type)
            user.save()
                
            
            member=WorkerProfile(address= address,phone=contact,agency_name=agency,dob=dob,workexp=exp,typeofid=idtype,idproof=doc,category_id=cat,user=user,documents=cert)
            member.save()
            messages.info(request,'Thankyou!Please login')
            return redirect('workersignup')
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
     
            
    messages.error(request,'Invalid Username and Password')
    return render(request,'login.html')
  
@login_required(login_url='loginact')  
def addcat(request):
    cat = request.POST['category']
    c = ServiceCategory(name=cat)
    c.save()
    messages.info(request, 'New Category Added!!!!!!')
    return redirect('addcategory')




@login_required(login_url='loginact')
def useredit(request,pk):
        u= UserProfile.objects.get(id=pk)
        return render(request,'useredit.html',{'u':u})

@login_required(login_url='loginact')
def useredit1(request,pk):
    if request.method == 'POST':
        u = UserProfile.objects.get(id=pk)
        v=CustomUser.objects.get(id=u.user_id)
        v.first_name = request.POST['fname']
        v.last_name = request.POST['lname']
        v.username = request.POST['uname']
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
        
  

@login_required(login_url='loginact')
def showuser(request):
    return render(request,'showuser.html')




@login_required(login_url='loginact')

def workercard(request,pk):
    if request.user.is_authenticated:
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
    else:

        return redirect("home")


@login_required(login_url='loginact')
def workercardbyuser(request,pk):
    profile = get_object_or_404(WorkerProfile, id=pk)
    fname = request.user.first_name.capitalize()
    lname=request.user.last_name
    uname=request.user.username
    email=request.user.email
    ph=profile.phone
    address = profile.address
    cat=profile.category.name
    exp=profile.workexp
    cert=profile.documents.url
    context = {
        'profile':profile,'fname':fname,'lname':lname,'uname':uname,'email':email,'phone':ph,'address':address,'cat':cat,'exp':exp,'cert':cert
        
       
    }
    return render(request,'workercardbyuser.html',context)


@login_required(login_url='loginact')
def workercardworker(request,pk):
    if request.user.is_authenticated:
        profile = WorkerProfile.objects.get(id=pk)
        fname = request.user.first_name.capitalize()
        lname=request.user.last_name
        uname=request.user.username
        email=request.user.email
        ph=profile.phone
        address = profile.address
        cat=profile.category.name
        agency=profile.agency_name
        exp=profile.workexp
        cert=profile.documents.url

        
        context = {
            'profile':profile,'fname':fname,'lname':lname,'uname':uname,'email':email,'phone':ph,'address':address,'cat':cat,'agency':agency,'exp':exp,'cert':cert
            
        
        }
        return render(request,'workercardworker.html',context)
    else:
        return redirect("home")






@login_required(login_url='loginact')
def workeredit(request,pk):
        e= WorkerProfile.objects.get(id=pk)
        c=ServiceCategory.objects.all()
        v=CustomUser.objects.get(id=e.user_id)
        return render(request,'workeredit.html',{'e':e,'c':c,'v':v})


@login_required(login_url='loginact')
def workeredit1(request, pk):
    if request.method == 'POST':
        e = WorkerProfile.objects.get(id=pk) 
        v = CustomUser.objects.get(id=e.user_id)
        
        v.first_name = request.POST.get('fname', '')
        v.last_name = request.POST.get('lname', '')
        v.username = request.POST.get('uname', '')
        v.email = request.POST.get('emailid', '')

        e.address = request.POST.get('address', '')
        e.phone = request.POST.get('ph', '')
        e.workexp = request.POST.get('exp', '')

        category_id = request.POST.get('cat', '')
        if not category_id:
            # Set a default category if none is provided
            default_category = ServiceCategory.objects.get(name='Default Category')
            e.category = default_category
        else:
            # Set the received category
            category = ServiceCategory.objects.get(id=category_id)
            e.category = category
        category_name = request.POST.get('cat', '')
        print("Received Category Name:", category_name)

        try:
            category = ServiceCategory.objects.get(name=category_name)
        except ServiceCategory.DoesNotExist:
            print("Category does not exist:", category_name)
       
        if 'certificates' in request.FILES:
            uploaded_certificates = request.FILES['certificates']
            print("Uploaded Certificate File Name:", uploaded_certificates.name)

            file_name, file_extension = os.path.splitext(uploaded_certificates.name.lower())

            # Validate file type by extension
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.txt']
            if file_extension not in allowed_extensions:
                error = "Invalid file type. Please upload an image, PDF, or text file."
                return render(request, 'workeredit.html', {'e': e, 'error': error, 'v': v})

            # Save the file
            storage = FileSystemStorage()
            file_path = os.path.join('certificates', str(e.id), f"{file_name}{file_extension}")
            storage.save(file_path, uploaded_certificates)

            print("Certificate File Path:", file_path)

            # Remove previous file, if any
            if e.documents and os.path.isfile(e.documents.path):
                os.remove(e.documents.path)

            # Update the certificate field in the profile
            e.documents = file_path

        # Handle file upload for 'Upload ID Proof'
        if 'idproof' in request.FILES:
            uploaded_idproof = request.FILES['idproof']
            print("Uploaded ID Proof File Name:", uploaded_idproof.name)

            idproof_name, idproof_extension = os.path.splitext(uploaded_idproof.name.lower())

            # Validate file type by extension
            allowed_idproof_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.txt']
            if idproof_extension not in allowed_idproof_extensions:
                error = "Invalid file type for ID proof. Please upload an image, PDF, or text file."
                return render(request, 'workeredit.html', {'e': e, 'error': error, 'v': v})

            storage = FileSystemStorage()
            idproof_path = os.path.join('idproofs', str(e.id), f"{idproof_name}{idproof_extension}")
            storage.save(idproof_path, uploaded_idproof)

            print("ID Proof File Path:", idproof_path)

            if e.idproof and os.path.isfile(e.idproof.path):
                os.remove(e.idproof.path)

            # Update the certificate field in the profile
            e.idproof = idproof_path

        
        

        e.save()
        v.save()

        error = "no"
        return render(request, 'workeredit.html', {'e': e, 'error': error, 'v': v})


        
        # return redirect('workeraction1')
    


@login_required(login_url='loginact')
def showusers(request):
    u = UserProfile.objects.all()
    return render(request,'showusers.html',{'u':u})

@login_required(login_url='loginact')
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
 

@login_required(login_url='loginact')
def addservice2(request):
    if request.method == 'POST':
        title1 = request.POST['sername'].capitalize()
        description1 = request.POST['desc']
        duration1 = request.POST['duration']
        price1 = request.POST['price']
        image1 = request.FILES['serimage']


        user = request.user
        worker_profile = WorkerProfile.objects.get(user=user)

        category1 = worker_profile.category

        p = Service(
            title=title1,
            description=description1,
            price=price1,
            image=image1,
            duration=duration1,
            category=category1,
            worker=worker_profile  
        )
        p.save()
        messages.info(request, 'New Service has been added!')
        return render(request, 'addserviceworker.html', {'worker_category': category1})

    return render(request, 'addserviceworker.html')

@login_required(login_url='loginact')
def addserviceworker(request):
    
    user = request.user

  
    worker_profile = WorkerProfile.objects.get(user=user)


    worker_category = worker_profile.category

    return render(request, 'addserviceworker.html', {'worker_category': worker_category})


@login_required(login_url='loginact')
def addservice(request):
    c=ServiceCategory.objects.all()
    return render(request,'addservice.html',{'c':c})

@login_required(login_url='loginact')
def fitr(request,pk):
    ct = Service.objects.filter(category=pk)
    s=ServiceCategory.objects.all()

    return render(request,'fitr.html',{'s':s,'ct':ct})

@login_required(login_url='loginact')

def bookit(request,pk):
    q = get_object_or_404(Service, id=pk)
    return render(request,'bookingform.html',{'q':q})

@login_required(login_url='loginact')
def bookit1(request,pk):
   
    if request.method=='POST':
        a=request.POST['day']
        a1=request.POST['address']
        q = get_object_or_404(Service, id=pk)
        u=UserProfile.objects.get(user_id=request.user.id)
        worker = q.worker 
        b=Booking(date_booked=a,address=a1,service_id=q.id,customer_id=u.user_id,category_id=q.category_id,worker=worker)
        b.save()
        error="no"
        return render(request,'bookingform.html',{'q':q,'error':error})


   
@login_required(login_url='loginact') 
def showworkers(request):
    w = WorkerProfile.objects.all()
    return render(request,'showworkers.html',{'w':w})
  
@login_required(login_url='loginact')  
def showworkersforuser(request):
    w = WorkerProfile.objects.all()
    return render(request,'showworkersforuser.html',{'w':w})

@login_required(login_url='loginact')
def workercard1(request,pk):
    pro1 = WorkerProfile.objects.get(user=request.user)
    return render(request,'showworkers.html',{'u':pro1})


@login_required(login_url='loginact')
def deleteworker(request,pk):
    c = WorkerProfile.objects.get(id=pk)
    c.delete()
    return redirect('showworkers')

@login_required(login_url='loginact')
def deleteuser(request,pk):
    c = UserProfile.objects.get(id=pk)
    c.delete()
    return redirect('showusers')


@login_required(login_url='loginact')
def logoutt(request):
    logout(request)
    return redirect('home')

@login_required(login_url='loginact')
def viewservices(request):
    v=Service.objects.all()
    return render(request,'viewservices.html',{'v':v})

@login_required(login_url='loginact')

def viewworkercards(request):
    cat = ServiceCategory.objects.all()
    w=WorkerProfile.objects.all()

    return render(request,'viewworkercards.html',{'w':w,'cat':cat})

# def myorderview(request):
#     b=Booking.objects.filter(customer_id=request.user.id)
#     return render(request,'myorderview.html',{'b':b})

@login_required(login_url='loginact')
def myorderview(request):
    # Filter Booking objects where the customer is the logged-in user and the status is 'pending', 'approved', or 'disapproved'
    bookings = Booking.objects.filter(customer_id=request.user.id, approval_status__in=['pending', 'approved', 'disapproved'])

    context = {
        'bookings': bookings,
    }

    return render(request, 'myorderview.html', context)
@login_required(login_url='loginact')
def deleteorder(request,pk):
    b = Booking.objects.get(id=pk)
    b.delete()
    return redirect('myorderview')

# def approve(request,pk):
#     try:
#         w=WorkerProfile1.objects.get(id=pk)
#         a=str(random.randint(100000, 999999))
#         use=CustomUser.objects.create_user(email=w.email,username=w.username,password=a,first_name=w.first_name,last_name=w.last_name,user_type='3')
#         usr=WorkerProfile(category=w.category,address=w.address,phone=w.phone,workexp=w.workexp,idproof=w.idproof,documents=w.documents)

#         usr.user=use
#         usr.save()
#         subject = 'Admin Approved'
#         message = f'Hello {usr.user.username},\nYour username: {usr.user.username}\nPassword: {a}'
#         recipient = use.email
#         send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])
#         w.delete()
#         messages.success(request, 'Approved!')
#         error = "no"
#     except Exception as e:
#         print(e)
#         messages.error(request, 'Something went wrong, Try Again')
#         error = "yes"

#     return render(request, 'approvaltable.html', {'error': error})

def approve(request, pk):
    try:
        w = WorkerProfile1.objects.get(id=pk)

        
        
        # Check if the category already exists
        if not w.category:
            category, created = ServiceCategory.objects.get_or_create(name=w.newcategory.strip())
            w.category = category
            w.save()

        usr = WorkerProfile(category=w.category, address=w.address, phone=w.phone, workexp=w.workexp, idproof=w.idproof, documents=w.documents)

        a = str(random.randint(100000, 999999))
        use = CustomUser.objects.create_user(email=w.email, username=w.username, password=a, first_name=w.first_name, last_name=w.last_name, user_type='3')
        usr.user = use
        usr.save()

        subject = 'Admin Approved'
        message = f'Hello {usr.user.username},\nYour username: {usr.user.username}\nPassword: {a}'
        recipient = use.email
        send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])

        w.delete()
        # messages.success(request, 'Approved!')
        error = "no"
    except Exception as e:
        print(e)
        messages.error(request, 'Something went wrong, Try Again')
        error = "yes"

    return render(request, 'approvaltable.html', {'error': error, 's': WorkerProfile1.objects.all()})






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
        agency=request.POST['agency']
        contact = request.POST['ph']
        exp=request.POST['exp']
        doc=request.FILES.get('doc')
        cat=request.POST['category']
        new_category_name=request.POST.get('newcategory','')
        cert=request.FILES.get('document')
    
        if CustomUser.objects.filter(username=user_name).exists():
            messages.info(request, 'This username already exists!')
            return redirect('workersignup')
        if CustomUser.objects.filter(email=email_id).exists():
            messages.info(request, 'This email-id already exists!')
            return redirect('workersignup')
  
        else:
             member1=WorkerProfile1(first_name=first_name,last_name=last_name,username=user_name,email=email_id,address= address,agency_name=agency,phone=contact,workexp=exp,idproof=doc,documents=cert,newcategory=new_category_name)
             
            # Check if the selected category is "Others"
             if cat == 'other'and new_category_name:
            # Add a new category request to NewCategoryRequest
                new_category_request = NewCategoryRequest(name=new_category_name, description='New category request')
                new_category_request.save()

                messages.info(request, f'New category request: {new_category_name}.')
                
          
               
               
             else:
                # If a different category is selected, use its ID
                member1.category_id = cat

             member1.save()
             
             messages.info(request, 'Please wait for admin approval for successful registration!')

             return redirect('workersignup')
    

    

@login_required(login_url='loginact')
def show_notification(request, display_location='approvaltable'):
    s = WorkerProfile1.objects.all()
    new_category_requests = NewCategoryRequest.objects.all()
   

 

    # if not s:
    #     messages.info(request, 'No New Registration Requests!')

    # template_name = 'approvaltable.html'  # Default template

    # if display_location == 'adminnotifications':
    #         # Assuming you have a specific message for new category requests
    #         messages.info(request, 'New Category Request: Your Message Here')

    #         template_name = 'adminnotifications.html'


    return render(request,'approvaltable.html',{'s': s, 'new_category_requests': new_category_requests})









@login_required(login_url='loginact')
def logoutt(request):
    logout(request)
    return redirect('home')

@login_required(login_url='loginact')
def servicebooking(request):
    # Assuming the worker's profile is associated with the service
    worker_profile = WorkerProfile.objects.get(user=request.user)
    
    # Filter Booking objects where the service is posted by the logged-in worker and is not approved
    s = Booking.objects.filter(
        service__worker=worker_profile,
        approval_status__in=['pending', 'approved', 'disapproved']
        
    )
    ab = s.filter(approval_status='pending').count()
    if s.exists():
        return render(request, 'viewservices.html', {'s': s, 'ab': ab})
    else:
        message = "No booking requests found."
        return render(request, 'viewservices.html', {'message': message})

@login_required(login_url='loginact')
def usercardbyworker(request, user_id):
    userprofile = get_object_or_404(UserProfile, user_id=user_id)
    fname = userprofile.user.first_name.capitalize()
    lname = userprofile.user.last_name
    uname = userprofile.user.username
    email = userprofile.user.email
    ph = userprofile.ph
    address = userprofile.address
    image = userprofile.profile_picture

    context = {
        'userprofile': userprofile,
        'fname': fname,
        'lname': lname,
        'uname': uname,
        'email': email,
        'ph': ph,
        'address': address,
        'image': image
    }

    return render(request, 'usercardbyworker.html', context)



@login_required(login_url='loginact')
def completefunction(request):
    # Filter Booking objects where the approval status is 'pending'
    com = Booking.objects.filter(approval_status='pending')
    return render(request, 'viewservices.html', {'com': com})

# def disapprovalorder(request,pk):
#     pre=Booking.objects.get(id=pk)
#     pre.is_approved=False
#     pre.save()
#     return redirect('servicebooking')

# def approvalorder(request,pk):
#     w=Booking.objects.get(id=pk)
#     w.is_approved=True
#     c=WorkerProfile.objects.get(user_id=request.user.id)
#     w.worker_id=c.id
#     w.save()
#     return redirect('servicebooking')

def disapprovalorder(request, pk):
    booking = get_object_or_404(Booking, id=pk)
    booking.approval_status = 'disapproved'
    booking.save()
    return redirect('servicebooking')

def approvalorder(request, pk):
    booking = get_object_or_404(Booking, id=pk)
    booking.approval_status = 'approved'
    c = WorkerProfile.objects.get(user_id=request.user.id)
    booking.worker_id = c.id
    booking.save()
    return redirect('servicebooking')


@login_required(login_url='loginact')
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

@login_required(login_url='loginact')
def update_passworduser(request):
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
                return redirect('update_passworduser')
            else:
                messages.error(request, 'New password and confirm new password do not match.')
        else:
            messages.error(request, 'Incorrect current password.')

    return render(request, 'changepassworduser.html')


  
@login_required(login_url='loginact')  
def update_passwordworker(request):
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
                return redirect('update_passwordworker')
            else:
                messages.error(request, 'New password and confirm new password do not match.')
        else:
            messages.error(request, 'Incorrect current password.')

    return render(request, 'changepasswordworker.html')


@login_required(login_url='loginact')
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

@login_required(login_url='loginact')
def usercardbyuser(request,pk):
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
    return render(request,'usercardbyuser.html',context)


@login_required(login_url='loginact')
def viewallbookings(request):
        bo = Booking.objects.all()
        return render(request,'viewallbookings.html',{'bo':bo})


# def viewprodadminandworker(request):

#     a=Service.objects.all()

#     return render(request,'viewprodadminandworker.html',{'a':a})


@login_required(login_url='loginact')
def viewprodworker(request):

    a=Service.objects.all()

    return render(request,'viewprodworker.html',{'a':a})



@login_required(login_url='loginact')
def feedback(request,pk):
    a = Booking.objects.get(id=pk)
    return render(request,'feedback.html',{'a':a})


@login_required(login_url='loginact')
def rating(request,pk):   
    if request.method=='POST':
        rating=request.POST['rating']
        comment=request.POST['comment']
        a = Booking.objects.get(id=pk)
        u=UserProfile.objects.get(user_id=request.user.id)
        d=Review(rating=rating,comment=comment,service_id=a.service_id,user_id=a.customer_id,booking_id=a.id)
        d.save()
        error="no"
        return render(request,'feedback.html',{'a':a,'error':error})
    
    

@login_required(login_url='loginact')
def viewfeedback(request):

    a=Review.objects.all()

    return render(request,'viewfeedback.html',{'a':a})


# def viewfeedbackworker(request):

#     a=Review.objects.all()

#     return render(request,'viewfeedbackworker.html',{'a':a})



@login_required(login_url='loginact')
def viewfeedbackworker(request):
    
    worker_profile = WorkerProfile.objects.get(user=request.user)

    # Get all reviews for services booked by customers for this worker
    reviews = Review.objects.filter(booking__worker=worker_profile)

    return render(request, 'viewfeedbackworker.html', {'reviews': reviews})

@login_required(login_url='loginact')
def viewfeedbackuser(request, service_id):
    # Assuming you have a URL pattern that includes the service_id parameter, like "/service_reviews/<int:service_id>/"
    # Retrieve the service based on the service_id
    service = Service.objects.get(pk=service_id)

    # Query reviews for the specific service
    reviews = Review.objects.filter(service=service)

    # Pass the reviews to the template
    return render(request, 'viewfeedbackuser.html', {'reviews': reviews})
    

@login_required(login_url='loginact')
def viewcategoryfeedbackadmin(request, service_id):

    service = Service.objects.get(pk=service_id)

    # Query reviews for the specific service
    reviews = Review.objects.filter(service=service)

    # Pass the reviews to the template
    return render(request, 'viewcategoryfeedbackadmin.html', {'reviews': reviews})

    
 
@login_required(login_url='loginact')   
def serviceedit(request, service_id):
    # Retrieve the specific service using the service_id
    try:
        q = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        messages.error(request, f"Service with ID {service_id} does not exist.")
        return redirect('my_services')  # Redirect to the page displaying all services

    # Retrieve all service categories for dropdown
    c = ServiceCategory.objects.all()
    return render(request, 'serviceedit.html', {'q': q, 'c': c})





@login_required(login_url='loginact')
def serviceedit1(request, service_id):
    if request.method == 'POST':
        try:
            q = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            messages.error(request, f"Service with ID {service_id} does not exist.")
            return redirect('my_services') 

    
        q.title = request.POST['sername']
        q.description = request.POST['desc']
        q.price = request.POST['price']
        q.duration = request.POST['duration']

        category_id = request.POST.get('category')
        if category_id:
            category = ServiceCategory.objects.get(id=category_id)
            q.category = category

  
        if 'serimage' in request.FILES:
            q.image = request.FILES['serimage']

        q.save()
       
        return redirect('my_services')  
    

    error="no"
    return render(request, 'serviceedit.html', {'q': q,'error':error})


@login_required(login_url='loginact')
def delservice(request,pk):
    c = Service.objects.get(id=pk)
    c.delete()
    return redirect('my_services')


@login_required(login_url='loginact')
def my_services(request):
   
    user = request.user
    worker_profile = WorkerProfile.objects.get(user=user)

    
    services = Service.objects.filter(worker=worker_profile)

    return render(request, 'myservicesworker.html', {'s': services})


@login_required(login_url='loginact')

def service_provider_history(request, worker_id):
    worker = get_object_or_404(WorkerProfile, id=worker_id)
    bookings = Booking.objects.filter(worker=worker, is_completed=True)

    context = {
        'worker': worker,
        'bookings': bookings,
    }

    return render(request, 'service_provider_history.html', context)

def search_service_provider(request):
    if 'q' in request.GET:
        query = request.GET['q']
        workers = WorkerProfile.objects.filter(user__username__icontains=query)
       
       

        context = {
            'query': query,
            'workers': workers,
        }

        return render(request, 'search_results.html', context)

    return render(request, 'search_results.html')


# def complete_task(request, booking_id):
#     booking = get_object_or_404(Booking, id=booking_id)

#     # Check if the request is a POST request (i.e., form submission)
# def complete_task(request, booking_id):
#     booking = get_object_or_404(Booking, id=booking_id)

#     # # Check if the approval_status is 'approved'
#     # if booking.approval_status != 'approved':
#     #     # You may want to handle this case differently, perhaps show an error message
#     #     return render(request, 'approval_not_approved.html', {'booking': booking})

#     # Check if the request is a POST request (i.e., form submission)
#     if request.method == 'POST':
#         # Update the is_completed field
#         booking.is_completed = True
#         booking.save()

#         # You may also include additional logic here (e.g., sending notifications)

#         return redirect('servicebooking', booking_id=booking.id)

#     # Render a confirmation page or form
#     return render(request, 'markcomplete.html', {'booking': booking})

@login_required(login_url='loginact')
def complete_task(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        booking = get_object_or_404(Booking, id=booking_id)
        booking.is_completed = True
        booking.save()
    return redirect('servicebooking')



@login_required(login_url='loginact')
def view_posted_services(request, worker_id):
    worker = WorkerProfile.objects.get(id=worker_id)
    posted_services = Service.objects.filter(worker=worker)

    return render(request, 'view_posted_services.html', {'worker': worker, 'posted_services': posted_services})

# def delete_category(request, category_id):
#     category = get_object_or_404(ServiceCategory, id=category_id)
    
#     if request.method == 'POST':
#         category.delete()
#         return redirect('view_categories')
    
#     return redirect('view_categories')


@login_required(login_url='loginact')
def search_by_category(request):
    categories = ServiceCategory.objects.all()
    services = Service.objects.all()

    query_category = request.GET.get('category', None)

    if query_category:
        services = services.filter(category__name__icontains=query_category)

    return render(request, 'search_by_category.html', {'categories': categories, 'services': services, 'query_category': query_category})


@login_required(login_url='loginact')
def adminnotifications(request):
    
    new_category_requests = NewCategoryRequest.objects.all()
    ab1=WorkerProfile1.objects.all().count()

    context = {
        'new_category_requests': new_category_requests,'ab1':ab1
    }

    return render(request, 'adminnotifications.html', context)

@login_required(login_url='loginact')
def save_new_category(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id')

        try:

            new_category_request = NewCategoryRequest.objects.get(id=request_id)
            new_category_name = new_category_request.name

        
            category, created = ServiceCategory.objects.get_or_create(name=new_category_name)

     
            new_category_request.delete()

        
            messages.success(request, 'New category added successfully!')
            messages.success(request, 'You can now Approve the Worker.')

            return redirect('show_notification')
        except NewCategoryRequest.DoesNotExist:
      
            messages.error(request, 'Invalid request_id')

 
    return redirect('show_notification')


@login_required(login_url='loginact')
def delete_category_request(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id')

        
        category_request = get_object_or_404(NewCategoryRequest, id=request_id)


        worker_profiles = WorkerProfile1.objects.filter(newcategory=category_request.name)

        for worker_profile in worker_profiles:
            worker_profile.delete()

        category_request.delete()

        messages.success(request, 'New category request not approved. Registration request also rejected!')

      
        return redirect('show_notification')

    
    return redirect('show_notification')