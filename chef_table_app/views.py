from django.core.files.storage import FileSystemStorage
from django.http.response import JsonResponse
from django.shortcuts import render, HttpResponse, redirect

from chef_table_app.models import *


def chef_page(request):
    return render(request,'chef_page.html')


def login(request):
    return render(request,'loginindex.html')

# def logincode(request):
#     print(request.POST)
#     username=request.POST['mail']
#     pwd=request.POST['Password']
#     ob=login_table.objects.filter(username=username,password=pwd)
#     if ob.exists():
#         ob1 = login_table.objects.get(username=username, password=pwd)
#         request.session['lid']=ob1.id
#         if ob1.type == 'admin':
#             return redirect('/adminhome')
#         elif ob1.type == 'user':
#             return redirect('/userhome')
#         elif ob1.type == 'chef':
#             return redirect('/chefhome')
#
#         else:
#             return redirect('/login')
#     else:
#         return redirect('/login')



def logincode(request):
    if request.method == 'POST':
        username = request.POST.get('mail')
        pwd = request.POST.get('Password')
        ob = login_table.objects.filter(username=username, password=pwd)

        if ob.exists():
            ob1 = login_table.objects.get(username=username, password=pwd)
            request.session['lid'] = ob1.id
            if ob1.type == 'admin':
                return redirect('/adminhome')
            elif ob1.type == 'user':
                return redirect('/userhome')
            elif ob1.type == 'chef':
                return redirect('/chefhome')
            elif ob1.type == 'blocked':
                return redirect('/login?error=blocked')
            else:
                return redirect('/login')
        else:
            # Redirect back to login with error message
            return redirect('/login?error=invalid')
    else:
        return redirect('/login')

def adminhome(request):
    a=UserTable.objects.all()
    us=a.count()
    request.session['user']=us


    cc=ChefTable.objects.filter(LOGIN__type='chef')
    cccount=cc.count()
    request.session['cccount']=cccount
    return render(request,'admin/aindex.html',{'user':us,'cccount':cccount})

def admin_view_user(request):
    ob=UserTable.objects.all()
    return render(request,'admin/users.html',{"val":ob})


def register(request):
    return render(request,'registration/userreg.html')

def registerchef(request):
    return render(request,'registration/chefreg.html')




def reg_code_user(request):
    # uname=request.POST['username']
    pwrd=request.POST['password']
    name=request.POST['name']
    place=request.POST['place']
    landmark=request.POST['post']
    gender=request.POST['gender']
    hn=request.POST['pin']
    email=request.POST['email']
    phone=request.POST['phone']

    aa=login_table.objects.filter(username=email)
    if aa.exists():
        return redirect('/register')

    ob=login_table()
    ob.username=email
    ob.password=pwrd
    ob.type="user"
    ob.save()

    ob1=UserTable()
    ob1.name =name
    ob1.gender =gender
    ob1.place =place
    ob1.house_number =hn
    ob1.landmark =landmark
    ob1.phone =phone
    ob1.email = email
    ob1.LOGIN=ob
    if 'img' in request.FILES:
        img=request.FILES['img']
        fs=FileSystemStorage()
        fn=fs.save(img.name,img)
        ob1.image=fn
    else:
        ob1.image="pic.jpg"

    ob1.save()
    return redirect('/login')

def reg_code_chef(request):
    # uname=request.POST['username']
    pwrd=request.POST['password']
    name=request.POST['name']
    place=request.POST['place']
    qualification=request.POST['qualification']
    gender=request.POST['gender']
    experience=request.POST['experience']
    email=request.POST['email']
    phone=request.POST['phone']

    aa = login_table.objects.filter(username=email)
    if aa.exists():
        return redirect('/register')

    ob=login_table()
    ob.username=email
    ob.password=pwrd
    ob.type="pending"
    ob.save()

    ob1=ChefTable()
    ob1.LOGIN=ob
    ob1.name =name
    ob1.gender =gender
    ob1.place =place
    ob1.Qualification = qualification
    ob1.Experience = experience
    ob1.phone = phone
    ob1.email =email

    if 'img' in request.FILES:
        img=request.FILES['img']
        fs=FileSystemStorage()
        fn=fs.save(img.name,img)
        ob1.image=fn
    else:
        ob1.image="pic.jpg"

    ob1.save()
    return HttpResponse('''<script>alert("added");window.location='/login'</script>''')


# def view_user(request):
#     a=UserTable.objects.all()
#     return render(request,'admin/view user.html',{'data':a})



def view_user(request):
    users = UserTable.objects.all().order_by('-id')  # Fetch all users ordered by ID in descending order
    return render(request, 'admin/view user.html', {'data': users})
def view_chef(request):
    a=ChefTable.objects.all().order_by('-id')
    return render(request,'admin/view chef.html',{'data':a})

def approve_chef(request,id):
    a=login_table.objects.filter(id=id).update(type='chef')
    return redirect('/view_chef')

def reject_chef(request,id):
    a=login_table.objects.filter(id=id).update(type='pending')
    return redirect('/view_chef')



def chefhome(request):
    a=ChefTable.objects.get(LOGIN_id=request.session['lid'])
    a = UserTable.objects.all()
    us = a.count()
    request.session['user'] = us

    return render(request,'chef/cindex.html',{'data':a,'user':us})

def userhome(request):
    return render(request,'user/index.html')

def c_profile(request):
    a=ChefTable.objects.get(LOGIN_id=request.session['lid'])
    return render(request,'chef/profile.html',{'profile':a})


def checkemail(request):
    # if request.method == 'GET':
    #     post_id = request.GET['post_id']
    #     likedpost = Post.objects.get(pk=post_id)  # getting the liked posts
    #     m = Like(post=likedpost)  # Creating Like Object
    #     m.save()  # saving it to store in database
    #     return HttpResponse("Success!")  # Sending an success response
    # else:
    #     return HttpResponse("Request method is not a GET")


    username  = request.GET['email']
    print(username)
    data = {
        'is_taken': login_table.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message']="A user with this email already exists."

        # return HttpResponse("A user with this username already exists.")
    return JsonResponse(data)

def block_user(request,id):
    ob=login_table.objects.get(id=id)
    ob.type='blocked'
    ob.save()
    return redirect("/view_user")



def unblock_user(request,id):
    ob = login_table.objects.get(id=id)
    ob.type = 'user'
    ob.save()
    return redirect("/view_user")

def history_chef(request,id):
    request.session['cid']=id
    ob=BookingTable.objects.filter(SHEDULE__CHEF__id=id)
    for i in ob:
        ob1=BookingDetailsTable.objects.filter(BOOKING__id=i.id)
        i.c=len(ob1)
    return render(request,"admin/viewhistory.html",{"val":ob})