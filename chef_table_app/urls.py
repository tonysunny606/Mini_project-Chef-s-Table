from django.urls import path
from chef_table_app import views

urlpatterns = [
    path('',views.chef_page),
    path('login',views.login),
    path('checkemail',views.checkemail),
    path('logincode',views.logincode),
    path('adminhome',views.adminhome),
    path('userhome',views.userhome),
    path('chefhome',views.chefhome),
    path('register',views.register),
    path('registerchef',views.registerchef),
    path('reg_code_user',views.reg_code_user),
    path('reg_code_chef',views.reg_code_chef),
    path('admin_view_user',views.admin_view_user),
    path('view_user',views.view_user),
    path('view_chef',views.view_chef),
    path('c_profile',views.c_profile),
    path('approve_chef/<id>',views.approve_chef),
    path('reject_chef/<id>',views.reject_chef),
    path('block_user/<id>',views.block_user),
    path('unblock_user/<id>',views.unblock_user),
    path('history_chef/<id>',views.history_chef),

]