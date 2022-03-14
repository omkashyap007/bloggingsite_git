from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from datetime import datetime
from .models import Post, Preference, Comment, Hashtag, Fame
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.core.paginator import Paginator
from blog.scripts import CreateHashtagList, CreateOrAddHashtag
from blog.forms import PostCreateForm , PostUpdateForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    ordering = ["-date_posted", "-likes"]
    paginate_by = 7

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_input = ""
        context["search_input"] = None
        context["users"] = None
        context["searched_posts"] = None
        context["seach_type"] = None
        return context


def UserPostListView(request, username):
    user = User.objects.filter(username=username).first()
    posts = Post.objects.filter(author=User.objects.filter(
        username=username).first()).order_by("-date_posted")
    context = {"posts": posts, "user": user}
    return render(request, "blog/user_posts.html", context)


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(post=kwargs["object"])[::-1]
        hashtag_set = kwargs["object"].hashtags.all()
        context["comments"] = comments
        context["length"] = len(comments)
        context["hashtag_set"] = hashtag_set
        return context

# blog/post_form.html


def CreatePost(request):
    form = PostCreateForm()
    if request.method == "POST":
        form = PostCreateForm(request.POST , request.FILES)
        post_image = request.FILES.get("postimage")
        if form.is_valid():
            title_text_color = request.POST.get("title_text_color") 
            content_text_color = request.POST.get("content_text_color")
            post = Post(title=form.instance.title,
                        content=form.instance.content, author=request.user ,
                        title_text_color = title_text_color ,
                        content_text_color = content_text_color ,
                        postimage = post_image )
            post.save()
            list_hashtags = CreateHashtagList(request.POST.get("hashtags"))
            for i in list_hashtags:
                hashtag = Hashtag.objects.filter(title=i)  # quertyset .
                count = hashtag.count()
                if count:
                    post.hashtags.add(hashtag.first().id)
                if not count:
                    hashtag = Hashtag(title=i)
                    hashtag.save()
                    post.hashtags.add(hashtag.id)
            return redirect("blog-home")
    else:
        form = PostCreateForm()
    context = {"form": form, "user": request.user}
    return render(request, "blog/create.html", context)

@login_required
def PostUpdate(request, pk):
    post = Post.objects.get(id = pk)
    form = PostUpdateForm(instance = post)
    title_text_color = post.title_text_color 
    content_text_color = post.content_text_color 
    
    hashtags = list(post.hashtags.all())
    hashtag_text = ""
    for i in hashtags:
        hashtag_text += f"#{i.title} "
    hashtag_text = hashtag_text.rstrip()
    
    if request.method == "POST" : 
        form = PostUpdateForm(request.POST,request.FILES  ,instance = post)
        title_text_color = request.POST.get("title_text_color")
        content_text_color = request.POST.get("content_text_color")
        if form.is_valid() :
            hashtag_list = CreateHashtagList(request.POST.get("hashtag_set"))
            CreateOrAddHashtag(hashtag_list, post)
            form.save()
            post.title_text_color = title_text_color
            post.content_text_color = content_text_color
            post.save()
            return redirect("post-detail" , pk)
        
        
    context = {"form" : form , 
               "title_text_color ": title_text_color , 
               "content_text_color" : content_text_color ,
               "hashtag_text" : hashtag_text , 
               }
    
    return render(request , "blog/post_update.html" , context)
    

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


def SearchData(request):
    search_input = request.POST.get("search_input")
    context = {}
    if request.method == "POST" and request.POST.get("search_input"):
        context["search_input"] = search_input
        have_value = False
        context["users"] = list(User.objects.filter(
            Q(username__startswith=search_input) |
            Q(username__icontains=search_input)
            ))
        if context["users"]:
            have_value = True
        context["searched_posts"] = set(Post.objects.filter(
            Q(title__startswith=search_input) |
            Q(title__icontains=search_input) |
            Q(title__endswith = search_input)|
            Q(hashtags__title__icontains =  search_input) 
            ).order_by("-likes"))
        if context["searched_posts"]:
            have_value = True
        if not have_value:
            messages.error(request, "The search has no item !")
            context = {"search_input" : search_input}
            return redirect(request.META["HTTP_REFERER"])
    return render(request , "blog/SearchPage.html" , context)
    

def BlogTypeView(request, hashtag):
    posts = (Hashtag.objects.filter(title=hashtag).first()).post_set.all()
    context = {"hashtag": hashtag, "posts": posts}
    return render(request, "blog/hashtag.html", context)


def about(request):
    return render(request, "blog/about.html")


def PostLike(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=pk)
        user_preference = ""

        try:
            preference_object = Preference.objects.get(
                user=request.user, post=post)
            preference_object.delete()
            post.likes -= 1
            post.save()
            return redirect("post-detail", pk)
        except:
            preference_object = Preference(
                post=post, user=request.user, preference=1)
            preference_object.save()
            post.likes += 1
            post.save()
            return redirect("post-detail", pk)

    else:
        messages.error(request, "You have to login first to like the post. ")
        return redirect("post-detail", pk)


def PostComment(request, pk):
    if request.user.is_authenticated:
        user = request.user
        pk = int(pk)
        the_comment = request.POST.get("comment")

        if the_comment:
            comment = Comment(writer=user,
                              post=Post.objects.filter(id=pk).first(), comment=the_comment)
            comment.save()
        else:
            messages.error(request, "The comment was empty !")
    else:
        messages.error(
            request, "You have to login first to comment on the post!")
    return redirect("post-detail", pk)


def DeleteComment(request, pk, post_pk):
    pk = int(pk)
    comment = get_object_or_404(Comment, id=pk)
    try:
        comment.delete()
    except:
        messages.error(request, "Unable to delete the Comment . Try later !")
        return redirect("post-detail", post_pk)

    return redirect("post-detail", post_pk)


def TypeableCheckbox(request):
    if request.method == "POST":
        hashtags = CreateHashtagList(request.POST.get("hashtags"))
        saved = False
        for i in hashtags:
            if not Hashtag.objects.filter(title=i).count():
                hashtag = Hashtag(title=i)
                hashtag.save()
                saved = True
            
        if saved:
            messages.success(
                request, "The new hashtags have been saved in the database !")
        if not saved:
            messages.error(
                request, "The hashtags you entered are already registered !")
    context = {}
    return render(request, "blog/create_checkbox.html", context)


def FollowUser(request, userid):
    try:
        current_user = User.objects.get(username=request.user.username)
    except:
        current_user = None

    if not current_user:
        messages.error(request, "You need to login to Follow the user !")
        return redirect("login-user")
    try:
        followed_user = User.objects.get(id=userid)
    except:
        followed_user = None
    if not followed_user:
        messages.error(
            request, "The user you are trying to follow is not found !")

    user_fame = Fame.objects.filter(user=followed_user).first()
    if current_user in user_fame.followers.all():
        messages.success(
            request, "You are already following {}".format(followed_user))
        return redirect(request.META["HTTP_REFERER"])

    followed_user.fame.followers.add(current_user.id)
    current_user.fame.following.add(followed_user.id)
    messages.success(request, "You followed {}".format(followed_user))
    return redirect(request.META["HTTP_REFERER"])


def UnFollowUser(request, userid):
    try:
        current_user = User.objects.get(id=request.user.id)
    except:
        current_user = None
    if not current_user:
        message.error(request, "You need to login to Unfollow !")
        return redirect("login-user")

    try:
        unfollowed_user = User.objects.get(id=userid)
    except:
        unfollowed_user = None

    if not unfollowed_user:
        messages.error(request, "The user you unfollowed was not found !")

    current_user.fame.following.remove(unfollowed_user.id)
    unfollowed_user.fame.followers.remove(current_user.id)

    messages.success(request, "You just unfollowed {}".format(unfollowed_user))
    return redirect(request.META["HTTP_REFERER"])


# om_kashyap007
# testingfortheuseritself123

# omkashyap007
# testing123

# newuser123
# testinguserpassword123
