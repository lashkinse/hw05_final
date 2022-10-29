from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from posts.models import Post, Group, User
from .forms import PostForm
from .utils import paginate_page


def index(request):
    template = "posts/index.html"
    posts = Post.objects.select_related("group", "author")

    page_obj = paginate_page(request, posts)

    context = {
        "page_obj": page_obj,
    }

    return render(request, template, context)


def group_posts(request, slug):
    template = "posts/group_list.html"
    group = get_object_or_404(Group, slug=slug)

    posts = group.posts.select_related("author")
    page_obj = paginate_page(request, posts)

    context = {
        "group": group,
        "page_obj": page_obj,
    }

    return render(request, template, context)


def profile(request, username):
    template = "posts/profile.html"
    author = get_object_or_404(User, username=username)

    posts = author.posts.select_related("group")
    page_obj = paginate_page(request, posts)

    context = {
        "author": author,
        "page_obj": page_obj,
    }

    return render(request, template, context)


def post_detail(request, post_id):
    template = "posts/post_detail.html"
    post = get_object_or_404(Post, id=post_id)

    context = {
        "post": post,
        "author": post.author,
        "user_can_edit": request.user == post.author,
    }

    return render(request, template, context)


@login_required
def create_post(request):
    template = "posts/create_post.html"
    form = PostForm(request.POST or None)

    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("posts:profile", username=request.user.username)

    context = {
        "form": form,
        "is_edit": False,
    }

    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    template = "posts/create_post.html"
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, instance=post)

    if post.author != request.user:
        return redirect("posts:post_detail", post_id=post_id)

    if form.is_valid():
        post.save()
        return redirect("posts:post_detail", post_id=post_id)

    context = {
        "post": post,
        "form": form,
        "is_edit": True,
    }

    return render(request, template, context)
