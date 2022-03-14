from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from multiselectfield import MultiSelectField
from colorfield.fields import ColorField
import datetime

class Post(models.Model) : 
    title = models.CharField(max_length = 150)
    content = models.TextField(max_length = 5000 )
    date_posted = models.DateTimeField(auto_now_add = datetime.datetime.now)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    likes = models.IntegerField(default = 0)
    hashtags = models.ManyToManyField("blog.Hashtag", verbose_name="the_Hashtags" , blank = True)
    updated = models.DateTimeField(auto_now = datetime.datetime.now , blank = True , null = True)
    title_text_color = ColorField( default = "#000000" , blank = True , null = True )
    content_text_color = ColorField( default = "#000000" , blank = True , null = True )
    postimage = models.ImageField( upload_to = "post_images" , default="blank.png")
         
    def __str__(self) : 
        return self.title

    def get_absolute_url(self) : 
        return reverse("post-detail" , kwargs = {"pk" : self.pk  })

class Preference(models.Model) : 
    preference= models.IntegerField(default = 0 )
    post = models.ForeignKey(Post , on_delete = models.CASCADE)
    user = models.ForeignKey(User , on_delete = models.CASCADE)
    date = models.DateTimeField(auto_now = True)
     
    def __str__(self) : 
        return str(self.user) + " " + str(["has not liked or disliked" , "liked" ,"disliked"][self.preference]) + "  the post."
    
    
class Comment(models.Model) : 
    writer = models.ForeignKey(User , on_delete = models.CASCADE )
    post = models.ForeignKey(Post , on_delete = models.CASCADE )
    comment = models.TextField(max_length = 150 , default = "")
    date_created = models.DateTimeField(auto_now = True)
    
    def __str__(self) : 
        return str(self.writer) + " commented "+ str(self.comment[:5]) + "****" + str(self.comment[-5:]) + " on -> "  + str(self.post.title)  

    class Meta :
        ordering = ["-id"]

class Hashtag(models.Model) :
    title = models.CharField(max_length = 40)
    date_created = models.DateTimeField(auto_now_add = True)
    
    def __str__(self) : 
        return str(self.title) + " -> " + str(self.id)
    

class Fame(models.Model):  
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    followers = models.ManyToManyField(User  ,related_name = "followers" , verbose_name = "followers" , blank = True )
    following = models.ManyToManyField(User  ,related_name = "following" , verbose_name = "following" , blank = True )
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)
    
    class Meta : 
        ordering = [ "-updated" , "-created"] 
    
    def __str__(self) : 
        return str(self.user.username) + " ->> has " + str(len(self.followers.all())) + " followers and " + str(len(self.following.all())) + " following" 

# create a friend table with a field time_added(auto_now = True ) 
# create a friend table with a ManyToManyField with user . 

# url defined with a name in urls.py 'post-detail'

# html ->
#   url_name 'post-detail' clicked.  
#   django will search for url in the urls.py with this name and the arguments passed into it. 

#   then a view name will be related to that url . then we will reach the view and the required 
#   will further move. 
# template -> url -> view 


# for reverse()
# redirecting sometimes you go to the reverse manner . 

# you give django a name of the view and it generates the proper url for that . Basically searches
# for the url in the urls.py 

# here view -> url -> template 