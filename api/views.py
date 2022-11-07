from blog.models import Post
from users.models import Profile
from rest_framework import status
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication 
from rest_framework.decorators import api_view , permission_classes
from rest_framework.filters import SearchFilter , OrderingFilter
from api.serializers import (
    PostSerializer , 
    UserRegisterSerializer ,
    UserLoginSerializer ,
    UserAccountSerializer ,
    UserProfileSerializer
)
@api_view(["GET"])
@permission_classes(())
def blogDetailView(request , *args , **kwargs) :
    id = kwargs["id"]
    print(id)
    response = {
        "data" : "Not Found" , 
        "error" : None ,
        "success" : False, 
        "status" : status.HTTP_404_NOT_FOUND , 
    }
    try :
        post = Post.objects.get(id = id)
    except : 
        return Response(
            response
        ) 
    if request.method == "GET": 
        serializer = PostSerializer(post)
        response["data"] = serializer.data
        response["error"] = None
        response["success"] = True
        response["status"] = status.HTTP_200_OK
        return Response(data = response , status = status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes((IsAuthenticated,))
def blogUpdateView(request , *args , **kwargs) :
    id = kwargs["id"]
    response = {
        "data" : "Not Updated" , 
        "error" : None ,
        "success" : False, 
        "status" : status.HTTP_404_NOT_FOUND , 
    }
    try : 
        post = Post.objects.get(id = id)
    except : 
        response["data"] = "No Post found with id {}".format(id)
        return Response(
            response
        ) 
        
    user = request.user
    if post.author != user :
        response["error"] = "You are not allowed to edit the post !"
        return Response(response)
    if request.method == "PUT" : 
        serializer = PostSerializer(post , data = request.data)
        if serializer.is_valid() :
            serializer.save()
            response["data"] = "Post Updated"
            response["error"] = None
            response["success"] = True
            response["status"] = status.HTTP_200_OK
            return Response(response)
        else : 
            response["error"] = serializer.errors
            print(response["error"]) 
            return Response(response)
    return Response("Other request methods are not allowed !")




@api_view(["DELETE"])
@permission_classes((IsAuthenticated,))
def blogDeleteView(request , *args , **kwargs) :
    id = kwargs["id"]
    response = {
        "data" : "Not Deleted" , 
        "error" : None ,
        "success" : False, 
        "status" : status.HTTP_404_NOT_FOUND , 
    }
    try :
        post = Post.objects.get(id = id)
    except :
        response["data"] = "There is no post with id = {}".format(id)
        return Response(
            response
        ) 
        
    user = request.user
    if post.author != user :
        response["error"] = "You are not allowed to delete the post !"
        return Response(response)
    if request.method == "DELETE" : 
        try : 
            post.delete()
            response["data"] = "Post Deleted"
            response["error"] = None
            response["success"] = True
            response["status"] = status.HTTP_200_OK
            return Response(response)
        except Exception as e : 
            response["error"] = str(e)
            return Response(response)
    return Response("Other request methods are not allowed !")


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def blogCreateView(request  , *args , **kwargs) :
    response = {
        "data" : "Not Created" , 
        "error" : None ,
        "success" : False, 
        "status" : status.HTTP_404_NOT_FOUND , 
    }
    if request.method == "POST" : 
        user = request.user
        post = Post(author = user)
        if not request.data : 
            response["status"] = status.HTTP_204_NO_CONTENT
            return Response(
                response
            )
        serializer = PostSerializer(post , data = request.data)
        if serializer.is_valid() :
            serializer.save()
            response["data"] = serializer.data
            response["success"] = True
            response["status"] = status.HTTP_201_CREATED
            return Response(response)
        else :
            response["error"] = serializer.errors
            return Response(response)
    else : 
        response["return_resposne"] = "Other request methods are not allowed !"
        return response(data = response , status = status.HTTP_404_NOT_FOUND)
    
@api_view(["POST" , ])
@permission_classes(())
def registerUserView(request , *args , **kwargs) : 
    response = {
        "data" : "Not Creted" , 
        "error" : None ,
        "success" : False, 
        "status" : status.HTTP_204_NO_CONTENT ,  
    }
    
    if request.method == "POST" :
        serializer = UserRegisterSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user = user)
            response["data"] = {
                "username" : serializer.validated_data.get("username"),
                "email": serializer.validated_data.get("email"),
                "token" : token.key, 
            }
            response["success"] = True
            response["status"] = status.HTTP_200_OK 
            return Response(data = response , status = status.HTTP_200_OK)
         
        else : 
            response["error"] = dict(serializer.errors)
            response["status"] = status.HTTP_400_BAD_REQUEST
            return Response(data = response , status = status.HTTP_400_BAD_REQUEST)
    else : 
        return Response("Other methods except POST are not allowed !")
    
@api_view(["POST"])
@permission_classes(())
def loginUserView(request , *args , **kwargs) : 
    response = {
        "data" : "InValid Login" , 
        "error" : None ,
        "success" : False, 
        "status" : status.HTTP_406_NOT_ACCEPTABLE , 
        "token" : None , 
    }
    
    if request.method == "POST" :
        serializer = UserLoginSerializer(data = request.data)
        if serializer.is_valid() : 
            token = serializer.save()
            response["data"] = "Successfull login"
            response["success"] = True
            response["token"] = token
            response["status"] = status.HTTP_200_OK
            return Response(data = response , status = status.HTTP_200_OK)
        else : 
            return Response(
                data = dict(serializer.errors)
            )
    else : 
        return Response("Other request methods are not allowed !")
    
class ApiBlogListView(ListAPIView) : 
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = ()
    permission_classes = ()
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter , OrderingFilter)
    search_fields = ("title" , "content" , "author__username")
blogListView = ApiBlogListView.as_view()

@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def getUserDetailView(request , *args , **kwargs) :
    response = {
        "data" : "User Not Found" , 
        "error" : None ,
        "success" : False, 
        "status" : status.HTTP_404_NOT_FOUND ,  
    } 
    try : 
        user = request.user
    except : 
        return Response(data =response)
    if request.method == "GET" : 
        serializer = UserAccountSerializer(user)
        response["data"] = serializer.data
        response["success"] = True
        response["status"] = status.HTTP_200_OK
        return Response(data = response , status = status.HTTP_200_OK)
    else : 
        return Response("Other methods are not allowed !")
    
@api_view(["PUT",])
@permission_classes((IsAuthenticated ,))
def updateUserDetailView(request , *args , **kwargs) :
    response = {
        "data" : "User Not Found" , 
        "error" : None ,
        "success" : False, 
        "status" : status.HTTP_404_NOT_FOUND ,  
    }
    try : 
        user = request.user
    except : 
        response["data"] = "InValid User !"
        response["status"] = status.HTTP_404_NOT_FOUND
        resposne["error"] = "There is no user related to the api request !"
        return Response(data = response)
    
    if request.method == "PUT" : 
        serializer = UserAccountSerializer(user , data = request.data)
        if serializer.is_valid() : 
            serializer.save() 
            response["success"] = True
            response["data"] = "User data updated successfully !"
            response["status"] = status.HTTP_200_OK
            return Response(data = response , status = status.HTTP_200_OK)
    else : 
        return Response("Other request methods are not allowed !")

@api_view(["GET",])
@permission_classes((IsAuthenticated ,))
def getUserProfileView(request, *args , **kwargs) : 
    response = {
        "data" : "User Not Found" , 
        "error" : None ,
        "success" : False, 
        "status" : status.HTTP_404_NOT_FOUND ,  
    }
    try : 
        user = request.user
    except :
        return Response(response , status = status.HTTP_404_NOT_FOUND)
    try : 
        profile = Profile.objects.get(user = user)
    except : 
        response["data"] = "User Profile Not Found !"
        return Response(data = response)
    if request.method == "GET" :
        serializer = UserProfileSerializer(profile)
        response["data"] = serializer.data
        response["success"] = True
        response["status"] = status.HTTP_200_OK
        return Response(data = response)
    else : 
        return Response("Other methods are not allowed !")

@api_view(["PUT"])
@permission_classes((IsAuthenticated,))
def updateUserProfileView(request, *args , **kwargs) :
    response = {
        "data" : "User Not Found" , 
        "error" : None ,
        "success" : False, 
        "status" : status.HTTP_404_NOT_FOUND ,  
    }
    try : 
        user = request.user
    except : 
        return Response(data = response)
    try : 
        profile = Profile.objects.get(user = user)
    except : 
        response["data"] = "User Profile not found !"
        response["error"] = "There is profile for the user {}".format(user.username)
        return Response(data = response , status = HTTP_404_NOT_FOUND)
    
    if request.method == "PUT" :
        serializer = UserProfileSerializer(profile , data = request.data)
        if serializer.is_valid():
            serializer.save()
            response["data"] = "User profile update successfully !"
            response["success"] = True
            response["status"] = status.HTTP_200_OK 
            return Response(response)
        else : 
            response["data"] = dict(serializer.errors)
            response["status"] = status.HTTP_400_BAD_REQUEST
            return Response(response)
    else : 
        return Response("Other request methods are not allowed !")
    