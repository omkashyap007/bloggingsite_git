from django.contrib import admin
from blog.models import Post , Preference , Comment , Hashtag  , Fame 

admin.site.register(Post)
admin.site.register(Preference)
admin.site.register(Comment)
admin.site.register(Hashtag)
admin.site.register(Fame)