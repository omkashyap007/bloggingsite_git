import os
from django.shortcuts import render ,get_object_or_404 
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages 
from django.shortcuts import redirect
from  .forms import UserRegisterForm 
from django.contrib.auth.decorators import login_required 
from users.forms import UserUpdateForm  , ProfileUpdateForm
from PIL import Image
from django.views.generic import DetailView
from users.models import Profile 
from django.contrib.auth import authenticate , login , logout
from users.forms import LoginForm 
from blog.scripts import getErrorList

def registerUser(request) :
    if request.method == "POST"   :
        form = UserRegisterForm(request.POST , request.FILES)
        if form.is_valid() : 
            saved_user = form.save()
            print(saved_user)
            username = request.POST.get("username")
            password = request.POST.get("password1")
            username = form.cleaned_data.get("username") 
            messages.success(request, "Account created for {}".format(username))
            messages.success(request , "Kindly update your Profile in Profile Page ")
            user = authenticate(username = username , password = password)
            print(user)
            login(request , user)
            return redirect("blog-home")
        else : 
            print(form.errors)
    else : 
        form = UserRegisterForm()
    return render(request , "users/register.html", {"form" : form})


def profileUser(request , username) :
    user = User.objects.filter(username = username).first()
    context = {"user" :user}
    return render(request , "users/profile.html" , context ) 

@login_required
def profileUpdate(request , userid) :
    if request.method == "POST" :
        user_update_form = UserUpdateForm(request.POST , instance = request.user)
        profile_update_form = ProfileUpdateForm(request.POST ,
                                               request.FILES ,
                                               instance = request.user.profile)
        if user_update_form.is_valid() and profile_update_form.is_valid() :
            user_update_form.save()
            profile_update_form.save()
            messages.success(request , "Your account has been updated!" )
            return redirect("profile-user" , request.user.username)
    else:
        user_update_form = UserUpdateForm(instance = request.user)
        profile_update_form = ProfileUpdateForm(instance = request.user.profile)
    context = {
        "user_update_form" : user_update_form ,
        "profile_update_form" : profile_update_form 
        }
    return render(request , 'users/profile_update_form.html' , context)



def DeleteAccount(request , pk) :
    pk = int(pk)
    username = User.objects.filter(id = pk).first()
    if request.user == username :
        context = {"pk" : pk , "username" : username }
        return render(request , "users/confirm_delete_account.html" , context )
    else : 
        messages.error(request , "You are not allowed to do delete someone's account !")
        return redirect("blog-home")
    
    
def ConfirmDeleteAccount(request , pk) : 
    pk = int(pk)
    user = get_object_or_404(User , id =pk)
    if request.user == user : 
        try :
            user.delete()
            return redirect("login-user")
        except :
            messages.error(request , "Unable to delete the account ! Kindly try again . ")
            return redirect("profile-user" , username=User.objects.filter(id=pk).first())
    else : 
        messages.error(request , "You are not allowed to delete someone else's account ! ")    
        return redirect("blog-home")
    return redirect("profile-user" , username = User.objects.filter(id=pk).first())
    
def PasswordResetDone(request) : 
    return render(request , "users/password_reset_done.html")
    
def PasswordResetComplete(request) : 
    return render(request , "users/password_reset_complete.html")

def UserFame(request , userid) : 
    user = User.objects.get(id = userid) 
    followers = user.fame.followers.all()
    followings = user.fame.following.all() 
    context = {"followers" : followers , "followings" : followings}
    
    return render(request , "users/famePage.html" , context )

def  LoginUser(request)  : 
    form = LoginForm()
    errors = []
    if request.method == "POST" : 
        form = LoginForm(request.POST)
        if form.is_valid(): 
            username = request.POST.get("username")
            password = request.POST.get("password")
            
            user = authenticate(username = username , password = password) 
            print(user)
            
            if user : 
                login(request , user)
                return redirect("blog-home")
            else : 
                message.error(request , "Kindly enter valid credentials !")   
        else : 
            errors = getErrorList(form.errors)
            
    context = {"form" : form , "errors" : errors}
    return render(request , "users/login.html" , context )

# dfadsFD235^&