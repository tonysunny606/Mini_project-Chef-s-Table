import datetime
from django.core.files.storage import FileSystemStorage
from django.http.response import JsonResponse
from django.shortcuts import render, HttpResponse, redirect

from django.core.paginator import Paginator
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


def events(request):
    ob=Events.objects.all()
    return render(request,'admin/manage_events.html',{"val":ob})

def add_events(request):
    ev=request.POST['ev']
    ob=Events()
    ob.event=ev
    ob.save()
    return redirect("/events")

def delete_events(request,id):

    ob=Events.objects.get(id=id)

    ob.delete()
    return redirect("/events")


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


def updateprofile(request):
    # id=request.POST['id']

    name=request.POST['name']
    place=request.POST['place']
    landmark=request.POST['post']
    gender=request.POST['gender']
    hn=request.POST['pin']
    email=request.POST['email']
    phone=request.POST['phone']



    ob1=UserTable.objects.get(id=id)
    ob1.name =name
    ob1.gender =gender
    ob1.place =place
    ob1.house_number =hn
    ob1.landmark =landmark
    ob1.phone =phone
    ob1.email = email

    if 'img' in request.FILES:
        img=request.FILES['img']
        fs=FileSystemStorage()
        fn=fs.save(img.name,img)
        ob1.image=fn
    else:
        ob1.image="pic.jpg"

    ob1.save()
    return redirect('/userhome')

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

    paginator = Paginator(users, 2)  # Show 5 posts per page

    page_number = request.GET.get('page')  # Get the page number from the request
    page_obj = paginator.get_page(page_number)  # Get the posts for that page

    # return render(request, 'myapp/view user.html', {'page_obj': page_obj})

    return render(request, 'admin/view user.html', {'data': page_obj})
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
    ob=ChefTable.objects.all()
    return render(request, 'user/userhome.html',{"ch":ob})

def userhome_search(request):
    ch=request.POST['ch']
    ob=ChefTable.objects.filter(name__icontains=ch)
    return render(request, 'user/userhome.html',{"ch":ob})

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

def view_profile(request):
    profile = UserTable.objects.get(LOGIN__id=request.session['lid'])
    return render(request, 'user/view_profile.html',{'profile':profile})

def edit_profile(request):
    user = UserTable.objects.get(LOGIN__id=request.session['lid'])
    return render(request, 'user/edit_profile.html', {'profile': user})

def edit_profile_post(request):
    # Fetch the logged-in user's profile
    profile = UserTable.objects.get(LOGIN__id=request.session['lid'])

    # Update the profile fields with form data
    profile.name = request.POST['name']
    profile.gender = request.POST['gender']
    profile.place = request.POST['place']
    profile.landmark = request.POST['landmark']
    profile.house_number = request.POST['house_number']
    profile.phone = request.POST['phone']
    profile.email = request.POST['email']

    # Handle image upload if provided
    if 'img' in request.FILES:
        img = request.FILES['img']
        fs = FileSystemStorage()
        fn = fs.save(img.name, img)
        profile.image = fn

    # Save the updated profile
    profile.save()

    # Redirect to the profile view page after updating
    return redirect('/view_profile')




def food_item_view(request):
    ob=FoodTable.objects.filter(CHEF__LOGIN__id=request.session['lid'])
    return render(request, 'chef/food_items_view.html',{"data":ob})

def food_item_view_search(request):
    s=request.POST['s']
    ob=FoodTable.objects.filter(CHEF__LOGIN__id=request.session['lid'],Name__istartswith=s)
    return render(request, 'chef/food_items_view.html',{"data":ob,"s":s})


def delete_fooditem(request,id):

    ob=FoodTable.objects.get(id=id)
    ob.delete()
    return redirect("/food_item_view")



def edit_fooditem(request,id):
    request.session['fid']=id
    ob=FoodTable.objects.get(id=id)

    return render(request,"chef/food_items_update.html",{"i":ob})


def food_item_update(request):
    name=request.POST['name']
    cuisine=request.POST['cuisine']
    type=request.POST['type']
    Meals=request.POST['Meals']
    details=request.POST['details']
    price=request.POST['price']


    ob=FoodTable.objects.get(id=request.session['fid'])
    ob.Cuisine = cuisine
    ob.Type = type
    ob.Name = name
    ob.Details = details
    ob.Meals = Meals
    ob.Price = price
    if 'img' in request.FILES:
        img = request.FILES['img']
        ob.Image = img
    ob.Date=datetime.datetime.today()
    ob.save()


    return redirect("/food_item_view")

def food_item_view_post(request):
    name=request.POST['name']
    cuisine=request.POST['cuisine']
    type=request.POST['type']
    Meals=request.POST['Meals']
    details=request.POST['details']
    price=request.POST['price']
    img=request.FILES['img']

    ob=FoodTable()
    ob.CHEF = ChefTable.objects.get(LOGIN__id=request.session['lid'])
    ob.Cuisine = cuisine
    ob.Type = type
    ob.Name = name
    ob.Details = details
    ob.Meals = Meals
    ob.Price = price
    ob.Image = img
    ob.Date=datetime.datetime.today()
    ob.save()


    return redirect("/food_item_view")


def food_item_add(request):
    return render(request, 'chef/food_items.html')


def BookNow(request,id):
    request.session['cid']=id
    a=ChefTable.objects.get(id=id)
    b=Events.objects.all()


    return render(request, 'BookNow/select_occasion.html',{'data':a,'data1':b,"d":datetime.datetime.now().strftime("%Y-%m-%d")})


def BookNow_post(request):
    print(request.POST)
    id=request.POST['id']
    date=request.POST['date']
    meal=request.POST.getlist('meal')

    burners=request.POST['burners']

    a=BookingTable()
    a.USER=UserTable.objects.get(LOGIN_id=request.session['lid'])
    a.CHEF=ChefTable.objects.get(id=id)

    a.number_gas=burners
    a.Date=date
    a.Status='pending'
    a.save()
    request.session['bid']=a.id
    print(meal,"meal")
    for i in meal:
        mt=request.POST[i]
        ob=BookingTable1()
        ob.BOOKING = a
        ob.mealstype = i
        ob.serving_time =mt
        ob.save()
    return redirect('/Bookdishes')
def Bookdishes(request):
    cid=request.session['cid']
    ob=BookingTable1.objects.filter(BOOKING__id=request.session['bid'])
    res={"Breakfast":{},"Lunch":{},"Dinner":{}}
    for i in ob:

        res[i.mealstype]['status']=True
        ob1=FoodTable.objects.filter(CHEF__id=cid,Meals=i.mealstype)
        res[i.mealstype]['data'] = ob1
    return render(request,"user/select_dishes.html",{"data":res})






