import base64
from blog.models import Post
from users.models import Profile
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class PostSerializer(serializers.ModelSerializer):
 
    username = serializers.SerializerMethodField("getUsername")
    
    some_other_username = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Post
        fields = ["title", "content", "likes", "date_posted" , "username" , "some_other_username"]

    
    
    def get_some_other_username(self , instance):
        return instance.author.username
 
    def getUsername(self, instance) :
        return  instance.author.username
    
     

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={
            "input_type": "password",
        },
        write_only=True,
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]

        extra_kwargs = {
            "password": {"write_only": True},
        }

    def save(self):

        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError(
                {"password": "The two password fields do not match !"})

        email = self.validated_data["email"]
        user = User.objects.filter(email=email)
        if len(user) > 0:
            raise serializers.ValidationError(
                {"email": "User with the email {} already exists".format(email)})

        user = User(
            email=self.validated_data["email"],
            username=self.validated_data["username"],
        )

        user.set_password(password)
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer) :
    username = serializers.CharField(
        style = {
            "input_type" : "text" , 
        },
    )
    
    password = serializers.CharField(
        style = {
            "input_type" : "password" , 
        },
        write_only = True , 
    )
    
    class Meta : 
        fields = ["username" , "password"]
        
    def save(self) :
        username = self.validated_data.get("username")
        password = self.validated_data.get("password")
        
        try : 
            user = authenticate(username = username , password = password)
        except User.DoesNotExist :
            raise serializers.VaildationError("The User with the username {} does not exist !".format(username))
        token = Token.objects.get(user = user)
        return token.key
        
      
    
class UserAccountSerializer(serializers.ModelSerializer):
    
    profile_image = serializers.SerializerMethodField("displayImage")
    
    class Meta : 
        model = User 
        fields = ["username" , "email" , "profile_image" ,  "first_name" , "last_name"]
        
    def displayImage(self , instance) : 
        return base64.b64encode(instance.profile.image.read()).decode("utf-8")

        
class UserProfileSerializer(serializers.ModelSerializer) :
    # image = serializers.SerializerMethodField("getImage")
    class Meta : 
        model = Profile
        fields = ["image" ,
                  "website_link" ,
                  "github_link" , 
                  "twitter_link" ,
                  "instagram_link" , 
                  "facebook_link" , 
                  "phone" , 
                  "city" ,
                  "country" , 
                  "about_user"
                 ]
        
    # def getImage(self , instance) :
    #     return base64.b64encode(instance.image.read()).decode("utf-8")