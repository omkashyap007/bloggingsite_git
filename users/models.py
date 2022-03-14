from django.db import models
# we are going to extend the user model which was already created 
from django.contrib.auth.models import User
from PIL import Image
from blog.models import Post

    
# this user is the user created by the django itself . Means the user which is active. 
# the user is not the instance of User . Its the user which you can see in the homepage. 
# well its the User instance .But you can can't change its name .
# if profile.user == request.user : then you can change the profile else not . 


class Profile(models.Model) :
    user = models.OneToOneField(User , on_delete = models.CASCADE)
    image = models.ImageField(default= 'default.png' , upload_to = "profile_pics")
    about_user = models.CharField(default= "" , max_length = 500 , blank =True , null = True)
    country = models.CharField(default = "" , max_length = 100 , blank =True , null = True)
    phone = models.CharField(default ="" ,max_length = 10 , blank =True , null = True)
    city = models.CharField(default ="" , max_length = 100 , blank =True , null = True)
    profession = models.CharField(default = "" , max_length = 100 , blank =True , null = True) 
    website_link = models.URLField(default= "" , blank =True , null = True)
    linkedin_link = models.URLField(default= "" , blank =True , null = True)
    twitter_link = models.URLField(default= "" , blank =True , null = True)
    github_link = models.URLField(default= "" , blank =True , null = True)
    instagram_link = models.URLField(default= "" , blank =True , null = True)
    facebook_link = models.URLField(default= "" , blank =True , null = True)
    
    
    def __str__(self): 
        return "{} Profile".format(self.user.username)
    
    def save(self, *args, **kwargs): 
        super().save(*args, **kwargs)
        
        img = Image.open(self.image.path) 
        
        
        if img.height > 125 or img.width >125 : 
            output_size = (150 , 150)
            img.thumbnail(output_size)
            img.save(self.image.path)
