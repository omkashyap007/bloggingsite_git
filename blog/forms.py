from django import forms
from blog.models import Post
from blog.scripts import CreateHashtagList
from .models import Hashtag
from django.forms.widgets import NumberInput
from colorfield.widgets import ColorWidget
from colorfield.fields import ColorField


class PostCreateForm(forms.ModelForm) :
    title = forms.CharField(widget = forms.TextInput(attrs = {
        "placeholder" :
            "Write the title here ! Select color of your title from button next to input !" ,
        "label" : None ,
        "class" : "form-control"}
    ) ,
    help_text = None,
    max_length = 100 )
    
    content = forms.CharField(widget = forms.Textarea(attrs = {
        "placeholder" : 
            "Write your content here ! Select color of content from the button next to input !"  , 
        "rows" :10 ,
        "class" : "form-control"}) 
    )
    
    hashtags = forms.CharField(widget = forms.Textarea(attrs = {
                "placeholder" : "Add the hashtags here seperated with space or comma !" ,
                "rows" : 3,
                "class" : "form-control"
    }) , required = False )
    
    postimage = forms.ImageField(widget= forms.FileInput(attrs = {
            "value" : "Add Image" , 
            "class" : "form-control" , 
            "alt" : "Add Image",
            }), 
        required = False , help_text = None)
    
    
    class Meta :
        model = Post
        fields = ["title" , "content"  , "hashtags" , "postimage"]
        

            
    def clean_title(self) : 
        title = self.cleaned_data.get("title")
        if len(title) > 150 : 
            raise forms.ValidationError("The title of the post may only be upto 150 characters !")
        return title    
    

class PostUpdateForm(forms.ModelForm) : 
    title = forms.CharField(
        max_length = 150 , 
        widget = forms.TextInput( 
            attrs = { 
                "id" : "title_area" , 
                "class" : "form-control" ,
            }    
        ),
        required= True
    )
    
    content = forms.CharField(
        max_length = 5000,  
        widget = forms.Textarea(
            attrs = {
                "id" : "content_area" ,
                "class" : "form-control" ,
                "rows": "8" , 
            }
        ),
        required = True
    )

    postimage = forms.ImageField(
        widget= forms.FileInput(
            attrs = {
                "id" : "post_image" , 
                "class" : "form-control" , 
            }
        ),
        required = False
    )
    
    class Meta : 
        model = Post
        fields = ["title" , "content" , "postimage"]
        