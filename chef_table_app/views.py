import datetime
from django.core.files.storage import FileSystemStorage
from django.http.response import JsonResponse
from django.shortcuts import render, HttpResponse, redirect

from django.core.paginator import Paginator
from chef_table_app.models import *
import razorpay


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



from django.db.models import Count
from django.db.models.functions import TruncMonth

def adminhome(request):
    a=UserTable.objects.all()
    us=a.count()
    request.session['user']=us
    cc=ChefTable.objects.filter(LOGIN__type='chef')
    cccount=cc.count()
    request.session['cccount']=cccount

    chef=[]
    ch_bookings_count=[]
    ob=ChefTable.objects.all()
    for i in ob:
        ob=BookingTable.objects.filter(Date__year=datetime.now().strftime("%Y"),CHEF__id=i.id)
        if len(ob)>0:
            ch_bookings_count.append(len(ob))
            chef.append(i.name)

    dict=[]
    for i in range(0,len(chef)):
        dict.append({"c":chef[i],"cc":ch_bookings_count[i]})
    sorted_data = sorted(dict, key=lambda x: x['cc'], reverse=True)
    cc=[0,0,0,0,0]
    cn=["","","","",""]
    for i in range(5):
        try:
            cc[i]=sorted_data[i]['cc']
            cn[i]=sorted_data[i]['c']
        except:
            break


    return render(request,'admin/aindex1.html',{'user':us,'cccount':cccount,'cc':cc,"cn":cn})

def admin_view_user(request):
    ob=UserTable.objects.all()
    return render(request,'admin/users.html',{"val":ob})



from .models import BookingTable
from collections import defaultdict
from datetime import datetime

def admin_view_report(request):
    # Get all bookings
    bookings = BookingTable.objects.all()

    # # Initialize a dictionary to hold counts of bookings per month
    # monthly_counts = defaultdict(int)
    #
    # for booking in bookings:
    #     # Use the actual date field instead of a string if Date is a DateField
    #     date_obj = booking.Date  # Assuming Date is a DateField
    #
    #     if date_obj:
    #         # Create a key in "Month Year" format
    #         month_year = date_obj.strftime('%B %Y')  # Create month-year key
    #         monthly_counts[month_year] += 1  # Increment count for this month
    #
    # # Extract months and counts for the chart
    # months = sorted(monthly_counts.keys(), key=lambda x: datetime.strptime(x, '%B %Y'))
    # bookings_count = [monthly_counts[month] for month in months]
    months=[1,2,3,4,5,6,7,8,9,10,11,12]
    bookings_count=[]
    for i in months:
        ob=BookingTable.objects.filter(Date__year=datetime.now().strftime("%Y"),Date__month=i)
        bookings_count.append(len(ob))

    chef=[]
    ch_bookings_count=[]
    ob=ChefTable.objects.all()
    for i in ob:
        ob=BookingTable.objects.filter(Date__year=datetime.now().strftime("%Y"),CHEF__id=i.id)
        if len(ob)>0:
            ch_bookings_count.append(len(ob))
            chef.append(i.name)

    dict=[]
    for i in range(0,len(chef)):
        dict.append({"c":chef[i],"cc":ch_bookings_count[i]})
    sorted_data = sorted(dict, key=lambda x: x['cc'], reverse=True)
    cc=[0,0,0,0,0]
    cn=["","","","",""]
    for i in range(5):
        try:
            cc[i]=sorted_data[i]['cc']
            cn[i]=sorted_data[i]['c']
        except:
            break


    return render(request, 'admin/chart.html', {
        'months': months,
        'bookings': bookings_count,'cc':cc,"cn":cn
    })




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


    return render(request, 'BookNow/select_occasion.html',{'data':a,'data1':b,"d":datetime.now().strftime("%Y-%m-%d")})


def BookNow_post(request):
    print(request.POST)
    id=request.POST['id']
    date=request.POST['date']
    mem=request.POST['mem']
    meal=request.POST.getlist('meal')

    burners=request.POST['burners']

    a=BookingTable()
    a.USER=UserTable.objects.get(LOGIN_id=request.session['lid'])
    a.CHEF=ChefTable.objects.get(id=id)

    a.number_gas=burners
    a.Date=date
    a.num_mem=mem
    a.Status='pending'
    a.save()
    request.session['mem']=mem
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



def Order_dishes(request):
    bf=request.POST.getlist('bf')
    lunch=request.POST.getlist('lunch')
    dinner=request.POST.getlist('dinner')
    print(bf)
    print(lunch)
    print(dinner)
    obb = BookingDetailsTable.objects.filter(BOOKING__id=request.session["bid"])
    if len(obb)==0:
        for i in bf:
            ob=BookingDetailsTable()
            ob.BOOKING_id=request.session['bid']
            ob.FOOD_id=i
            obf=FoodTable.objects.get(id=i)
            cou=request.POST["c"+str(i)]
            ob.Count = cou
            ob.Price = int(cou)*int(obf.Price)
            ob.save()
        for i2 in lunch:
            ob = BookingDetailsTable()
            ob.BOOKING_id=request.session['bid']
            ob.FOOD_id = i2
            obf = FoodTable.objects.get(id=i2)
            cou = request.POST["c" + str(i2)]
            ob.Count = cou
            ob.Price = int(cou) * int(obf.Price)
            ob.save()
        for i3 in dinner:
            ob = BookingDetailsTable()
            ob.BOOKING_id = request.session['bid']
            ob.FOOD_id = i3
            obf = FoodTable.objects.get(id=i3)
            cou = request.POST["c" + str(i3)]
            ob.Count = cou
            ob.Price = int(cou) * int(obf.Price)
            ob.save()


    obb=BookingTable.objects.get(id=request.session["bid"])

    obb3=BookingDetailsTable.objects.filter(BOOKING_id=request.session["bid"])
    data=[]
    grandtotal=0
    for i in obb3:
        grandtotal=grandtotal+float(i.Price)
        r={"id":i.id,"food":i.FOOD.Name,"actualprice":i.FOOD.Price,"Count":i.Count,"total":str(i.Price)}
        data.append(r)
    gst=round(grandtotal*0.05,2)
    grandtotal_gst=grandtotal+gst

    return render(request,'user/Bill_info.html',{"bookinfo":obb,"bookmore":data,"grandtotal":grandtotal,"grandtotal_gst":grandtotal_gst,"gst":gst})



def chef_view_booking(request):

    obb3=BookingTable.objects.filter(CHEF__LOGIN__id=request.session["lid"])
    for i in obb3:
        ob=BookingDetailsTable.objects.filter(BOOKING__id=i.id)
        t=0
        for j in ob:
            t=t+int(j.Price)
        i.p=t+(t*.05)

    return render(request,"chef/view_booking.html",{"data":obb3})



def chef_view_booking_search(request):
    s=request.POST['s']
    obb3=BookingTable.objects.filter(CHEF__LOGIN__id=request.session["lid"],Date=s)
    for i in obb3:
        ob=BookingDetailsTable.objects.filter(BOOKING__id=i.id)
        t=0
        for j in ob:
            t=t+int(j.Price)
        i.p=t+(t*.05)

    return render(request,"chef/view_booking.html",{"data":obb3,"s":s})




def view_dishes_chef(request,id):
    print(id)
    request.session['bid']=id
    obb3=BookingDetailsTable.objects.filter(BOOKING__id=id)
    l=[]
    print(obb3,"====")
    for i in obb3:
        l.append(i.FOOD.id)
    res = {"Breakfast": {}, "Lunch": {}, "Dinner": {}}
    ob=["Breakfast","Lunch","Dinner"]
    sid=0
    for i in ob:

        ob1 = FoodTable.objects.filter( Meals=i,id__in=l)
        print(ob1)

        res[i]['data'] = ob1
        if len(ob1)>0:
            res[i]['status'] = True

    obb = BookingTable.objects.get(id=id)

    obb3 = BookingDetailsTable.objects.filter(BOOKING_id=id)
    data = []
    grandtotal = 0
    for i in obb3:
        grandtotal = grandtotal + float(i.Price)
        r = {"id": i.id, "food": i.FOOD.Name,"im":i.FOOD.Image.url, "actualprice": i.FOOD.Price,"c":i.Count,
             "total": str(i.Price)}
        data.append(r)
    gst=(grandtotal*0.05)
    grandtotal_gst = grandtotal + gst

    # return render(request, 'user/Bill_info.html',
    #               {"bookinfo": obb, "bookmore": data, "grandtotal": grandtotal, "grandtotal_gst": grandtotal_gst})

    return render(request,"chef/view_dishes_chef.html",{"data":res,"bookinfo": obb, "bookmore": data, "grandtotal": grandtotal, "grandtotal_gst": grandtotal_gst,'gst':gst})

def view_booking_dishes_user(request,id):
    print(id)
    request.session['bid']=id
    obb3=BookingDetailsTable.objects.filter(BOOKING__id=id)
    l=[]
    print(obb3,"====")
    for i in obb3:
        l.append(i.FOOD.id)
    res = {"Breakfast": {}, "Lunch": {}, "Dinner": {}}
    ob=["Breakfast","Lunch","Dinner"]
    for i in ob:

        ob1 = FoodTable.objects.filter( Meals=i,id__in=l)
        print(ob1)
        res[i]['data'] = ob1
        if len(ob1)>0:
            res[i]['status'] = True

    obb = BookingTable.objects.get(id=id)

    obb3 = BookingDetailsTable.objects.filter(BOOKING_id=id)
    data = []
    grandtotal = 0
    for i in obb3:
        grandtotal = grandtotal + float(i.Price)
        r = {"id": i.id, "food": i.FOOD.Name,"im":i.FOOD.Image.url, "actualprice": i.FOOD.Price,"c":i.Count,
             "total": str(i.Price)}
        data.append(r)
    gst=(grandtotal*0.05)
    grandtotal_gst = grandtotal + gst
    s=False
    obs=None
    ps='na'
    try:
        obs = obb3[0].BOOKING.CHEF
        if obb.Status=='Accepted' :
            s = True

        if obb.Status=='paid' :
            s=True
            ps="p"

    except Exception as e:
        print(e)
        pass

    print("s",s,"ps",ps,"=======================")
    print("s",s,"ps",ps,"=======================")
    print("s",s,"ps",ps,"=======================")
    print("s",s,"ps",ps,"=======================")
    # return render(request, 'user/Bill_info.html',
    #               {"bookinfo": obb, "bookmore": data, "grandtotal": grandtotal, "grandtotal_gst": grandtotal_gst})

    return render(request,"user/view_dishes_chef.html",{"data":res,"bookinfo": obb, "bookmore": data, "grandtotal": grandtotal, "grandtotal_gst": grandtotal_gst,'gst':gst,"s":s,"obs":obs,"id":id,"ps":ps})

def accept_booking(request):
    ob=BookingTable.objects.get(id=request.session['bid'])
    ob.Status='Accepted'
    ob.save()
    return redirect("/chef_view_booking")

def reject_booking(request):
    ob=BookingTable.objects.get(id=request.session['bid'])
    ob.Status='Reject'
    ob.save()
    return redirect("/chef_view_booking")


def my_booking(request):

    obb3=BookingTable.objects.filter(USER__LOGIN__id=request.session["lid"])
    for i in obb3:
        ob=BookingDetailsTable.objects.filter(BOOKING__id=i.id)
        t=0
        for j in ob:
            t=t+int(j.Price)
        i.p=t+(t*.05)

    return render(request,"user/view_booking.html",{"data":obb3})



def my_booking_post(request):
    f=request.POST['fdate']
    t=request.POST['tdate']

    obb3=BookingTable.objects.filter(USER__LOGIN__id=request.session["lid"],Date__range=[f,t])
    for i in obb3:
        ob=BookingDetailsTable.objects.filter(BOOKING__id=i.id)
        t=0
        for j in ob:
            t=t+int(j.Price)
        i.p=t+(t*.05)

    return render(request,"user/view_booking.html",{"data":obb3})


def payment(request,id,amt):
    request.session['rid'] = id
    request.session['pay_amount'] = str(amt).split(".")[0]
    client = razorpay.Client(auth=("rzp_test_edrzdb8Gbx5U5M", "XgwjnFvJQNG6cS7Q13aHKDJj"))
    print(client)
    payment = client.order.create({'amount': request.session['pay_amount']+"00", 'currency': "INR", 'payment_capture': '1'})
    res=UserTable.objects.get(LOGIN__id=request.session['lid'])


    return render(request,'user/UserPayProceed.html',{'p':payment,'val':res,"lid":request.session['lid'],"id":request.session['rid']})

def on_payment_success(request):
    request.session['rid'] = request.GET['id']
    request.session['lid'] = request.GET['lid']
    # var = auth.authenticate(username='admin', password='admin')
    # if var is not None:
    #     auth.login(request, var)
    # amt = request.session['pay_amount']
    # ob=payment()
    # ob.date=datetime.datetime.now().today().date()
    # ob.time=datetime.datetime.now().today().time()
    # ob.ORDER=BookingTable.objects.get(id=request.session['rid'])
    # ob.status='paid'
    # ob.save()
    ob = BookingTable.objects.get(id=request.session['rid'])
    ob.Status = 'paid'
    ob.save()
    return HttpResponse('''
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@10">
                <script src="https://cdn.jsdelivr.net/npm/sweetalert2@10"></script>
                <script>
                    document.addEventListener("DOMContentLoaded", function() {
                        Swal.fire({
                            icon: 'success',
                            title: 'Booking Confirmed... !',
                            confirmButtonText: 'OK',
                            reverseButtons: true
                        }).then((result) => {
                            if (result.isConfirmed) {
                                window.location = '/my_booking';
                            }
                        });
                    });
                </script>
            ''')
def feedback(request,id):
    request.session['cid']=id



    return render(request,'user/feedback.html')


def add_feedback(request):
    bid = request.session['bid']
    fbk=request.POST['fbk']
    rating=request.POST['rating']

    ob=Feedback()
    ob.Feedback=fbk
    ob.BOOKING = BookingTable.objects.get(id=bid)
    ob.rating = rating
    ob.date =datetime.datetime.today()
    ob.save()





    return redirect("/view_booking_dishes_user/"+str(bid))

def add_complaint(request):
    bid = request.session['bid']
    comp=request.POST['comp']

    ob=Complient()
    ob.BOOKING= BookingTable.objects.get(id=bid)
    ob.reply="pending"
    ob.Complient=comp
    ob.date_replied = datetime.datetime.today()
    ob.date_submitted =datetime.datetime.today()
    ob.save()





    return redirect("/view_booking_dishes_user/"+str(bid))

def complaint_user(request):
    a=Complient.objects.all().order_by('-id')



    return render(request,'admin/complaint_user.html',{'data':a})




def complaint_user(request):
    a=Feedback.objects.all().order_by('-id')



    return render(request,'admin/feedback_user.html',{'data':a})



