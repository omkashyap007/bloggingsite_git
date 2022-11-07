from django.urls import path
from api import views as api_views

from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
path("blog/list/"            , api_views.blogListView   , name = "blog-list")       ,
path("blog-detail/<int:id>/" , api_views.blogDetailView , name = "blog-detail-api") , 
path("blog-update/<int:id>/" , api_views.blogUpdateView , name = "blog-update-api") , 
path("blog-delete/<int:id>/" , api_views.blogDeleteView , name = "blog-delete-api") , 
path("blog-create/"          , api_views.blogCreateView , name = "blog-create-api") , 

# accout section api
path("account/register/"     , api_views.registerUserView     , name = "account-register") , 
path("account/login/"        , api_views.loginUserView        , name = "account-login")    , 
path("account/"              , api_views.getUserDetailView    , name = "account-detail")   ,
path("account/update/"        , api_views.updateUserDetailView , name = "account-update")  ,

#profile section
path("account/profile/"        , api_views.getUserProfileView    , name = "account-profile-detail")  ,
path("account/profile/update"  , api_views.updateUserProfileView , name = "account-profile-update")  ,

]