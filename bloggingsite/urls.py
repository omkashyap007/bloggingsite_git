from django.contrib import admin
from django.urls import path ,include , re_path
from users import views as users_views 
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from blog import views as blog_views

from django.views.static import serve

urlpatterns = [
    # admin routing 
    path("admin/" , admin.site.urls) ,
    
    
    # authentication routing
    path("register/", users_views.registerUser, name = "register-user"),
    path("profile/<str:username>/" , users_views.profileUser , name = "profile-user"),
    path("login/",  users_views.LoginUser , name = "login-user"),
    path("logout/" , auth_views.LogoutView.as_view(template_name = 'users/logout.html') ,name = "logout-user"),
    path("profile/update/<int:userid>" , users_views.profileUpdate , name = "profile-update"),
    path("delete/account/<int:pk>/" , users_views.DeleteAccount , name = "delete-account") ,
    path("delete/account/confirm/<int:pk>/" , users_views.ConfirmDeleteAccount , name = "delete-account-confirm" ),
    path("fame/<int:userid>/" , users_views.UserFame , name = "fame-user") ,
    
    
    #blog routing .
    path("" , include("blog.urls")) ,
    
    
    #password resetting
    path("password-reset/" ,
          auth_views.PasswordResetView.as_view(template_name = "users/password_reset.html") ,
          name = "password_reset"
          ),
    # if the password reset is submitted . 
    # then it will redirect you to the password-reset-done page. 
    # and will send the request to the password_reset_comfirm page. 
    # actually i want to create a new page for the password reset page. 
    # thats easy actually . but don't know how to do it. 
    
    # the path below gives a template which tells that the password reset email has been sent
    # and you have to check the email for the instructions . 
    path("password-reset/done/" , 
         users_views.PasswordResetDone,
         name = "password_reset_done"),
    
     
    path("password-reset-confirm/<uidb64>/<token>/" ,
         auth_views.PasswordResetConfirmView.as_view(
         template_name = "users/password_reset_confirm.html"),
         name = "password_reset_confirm") , 
    
    path("password-reset-complete" ,
         users_views.PasswordResetComplete,
         name = "password_reset_complete"),
    
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root':settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]

urlpatterns = urlpatterns+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)