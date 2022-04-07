from django import forms 
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from users.models import Profile
from django.contrib.auth.forms import PasswordResetForm
from django.core.validators import RegexValidator
from users.scripts import correctPassword


PROFESSION_CHOICES = [ ('student', 'Student'),
                       ('web developer', 'Web Developer'),
                       ('machine learning engineer', 'Machine Learning Engineer'),
                       ('artifical intelligence engineer', 'Artifical Intelligence Engineer'),
                       ('data scientist', 'Data Scientist'),
                       ('data analyst', 'Data Analyst'),
                       ('economist', 'Economist'),
                       ('politician', 'Politician'),
                       ('professor', 'Professor'),
                       ('architect', 'Architect'),
                       ('doctor', 'Doctor'),
                       ('lawyer', 'Lawyer'),
                       ('engineer', 'Engineer'),
                       ('teacher', 'Teacher'),
                       ('police officer', 'Police Officer'),
                       ('nurse', 'Nurse'),
                       ('others' , 'Others'),
]


class UserRegisterForm(UserCreationForm) :
    
    username = forms.CharField(
        widget = forms.TextInput( 
            attrs = { 
                "id" : "register_username" , 
                "placeholder" : "Username !"
            }
        ),
        required = True , 
    )
    
    email = forms.EmailField(
        widget = forms.EmailInput(
            attrs = {
                "placeholder" : "Kindly enter your email !" ,
                "id" : "register_email"
            }
        ),
        required = True 
    )
    
    password1 = forms.CharField(
        min_length = 8 , 
        widget= forms.PasswordInput(
            attrs =  {
                "id" : "register_password_1" , 
                "placeholder" : "Create your password !" ,
                "oninput" : "checkPassword()" 
            }
        )
        ,
        required = True
    )
    password2 = forms.CharField(
        min_length = 8 ,
        widget= forms.PasswordInput(
            attrs =  {
                "id" : "register_password_2" , 
                "placeholder" : "Confirm your password  !",
                "oninput" : "checkConfirmPassword" , 
            }
        )
        ,
        required = True
    )
    
    class Meta : 
        model = User
        fields = ["username" , "email" , "password1" , "password2"]
    
    def clean_username(self) : 
        username = self.cleaned_data.get("username") 
        
        if len(username) > 30 : 
            raise forms.ValidationError("The username must be smaller than 30 characters !")
        user_count = User.objects.filter(username=  username ).count() 
        
        if user_count: 
            raise forms.ValidationError("This username already exists. Kindly Choose another one!")
        
        
        if not user_count: 
            return username
        return username
    
    def clean_email(self) : 
        email = self.cleaned_data.get("email")
        email_count = User.objects.filter(email = email).count() 
        
        if email_count: 
            raise forms.ValidationError("The email is already registered !")
        
        if not email_count:
            return email

        return email 
    
    def clean_password1(self):  
        password1 = self.cleaned_data.get("password1")
        if not password1 : 
            raise forms.ValidationError("Kindly enter the Password !")
        if len(password1) <8 : 
            raise forms.ValidationError("The lenght of the password must be greater than 8")
        return password1
        
    #newpsOYOIPU2342&(&*())
        
    def clean_password2(self) :
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if not password2 :
            raise forms.ValidationError("Kindly enter the Confirmation Password !")
        if password1 and password2  and not password1 == password2 : 
            raise forms.ValidationError("The two passwords didn't match !")
        
        return password2
        
class UserUpdateForm(forms.ModelForm) :
    username = forms.CharField() 
    email = forms.EmailField() 
    first_name = forms.CharField() 
    last_name = forms.CharField() 
    
    class Meta :
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                   )
        
class ProfileUpdateForm(forms.ModelForm) :
    image = forms.ImageField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$',
        message="Phone number must be entered in the format: '0123456789'.Only 10 digits allowed")
    phone = forms.CharField(required = False , validators=[phone_regex], max_length = 10) 
      
    about_user = forms.CharField(required = False , 
                          widget=forms.TextInput(attrs={'placeholder': 'Enter your bio'}),
                          max_length = 500)
    
    country = forms.CharField(required = False ,
        widget=forms.TextInput(attrs={'placeholder': "What's your country :"}))
    city = forms.CharField(required = False ,widget=forms.TextInput(attrs={'placeholder': 'Enter your city'}))
    
    phone = forms.IntegerField(required = False , 
        widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'}))
    
    profession = forms.CharField(label = "What's is your Profession ?" , 
                                 widget = forms.Select(choices = PROFESSION_CHOICES),
                                 required = True,
                                 )
    
    
    website_link = forms.URLField(required = False , 
    widget=forms.TextInput(attrs={'placeholder': 'Your Website link '}))
    linkedin_link = forms.URLField(required = False , 
    widget=forms.TextInput(attrs={'placeholder': 'Your Linked In link '}))
    twitter_link = forms.URLField(required = False , 
    widget=forms.TextInput(attrs={'placeholder': 'Your Twitter link '}))
    github_link = forms.URLField(required = False , 
    widget=forms.TextInput(attrs={'placeholder': 'Your Github link '}))
    instagram_link = forms.URLField(required = False , 
    widget=forms.TextInput(attrs={'placeholder': 'Your Instagram link '}))
    facebook_link = forms.URLField(required = False , 
    widget=forms.TextInput(attrs={'placeholder': 'Your Facebook link '}))
    
    
    
    class Meta : 
        model = Profile
        fields = ('image', 
                  'about_user',
                   'phone',
                   'country' ,
                   'city',
                   'profession',
                   'website_link',
                   'linkedin_link',
                   'twitter_link' , 
                   'github_link' ,
                   'instagram_link',
                   'facebook_link' ,
                   )
    
class LoginForm(forms.Form) : 
    username = forms.CharField(
        widget = forms.TextInput(
            attrs = { 
                    "placeholder" : "Enter the Username here !" , 
                    "id" : "login_username" , 
                    }
        ),
        required = True 
    )
    
    password = forms.CharField(
        widget= forms.PasswordInput( 
            attrs = {
                "placeholder" : "Enter the password here !" ,
                "id" : "login_password" , 
            }
        ),
        required = True ,
    )
    
    class Meta : 
        fields = ["username" , "password"] 
        
    def clean_username(self) : 
        username = self.cleaned_data.get("username")
        try : 
            user = User.objects.get(username = username)
        except : 
            user = None
        
        if not user: 
            raise forms.ValidationError("No user with this username !")
        
        return username
    
    def clean_password(self) : 
        password = self.cleaned_data.get("password")
        username = self.cleaned_data.get("username")
        
        if not password : 
            raise forms.ValidationError("Kindly enter the password !")
        try : 
            user = User.objects.get(username = username)
        except: 
            user = None
        
        if not user: 
            raise forms.ValidationError("Kindly enter the correct  username !") 
        if user and not user.check_password(password) : 
            raise forms.ValidationError("Invalid Password !") 
        
        return password 
# abcdABXD123#@