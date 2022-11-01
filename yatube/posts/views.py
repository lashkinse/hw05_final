from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page
from posts.models import Follow, Group, Post, User

from .forms import CommentForm, PostForm
from .utils import paginate_page


@cache_page(20, key_prefix="index_page")
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
    following = (
        request.user.is_authenticated
        and Follow.objects.filter(user=request.user, author=author).exists()
    )
    context = {"author": author, "page_obj": page_obj, "following": following}
    return render(request, template, context)


def post_detail(request, post_id):
    template = "posts/post_detail.html"
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm()
    comments = post.comments.all()
    context = {
        "post": post,
        "author": post.author,
        "form": form,
        "comments": comments,
    }
    return render(request, template, context)


@login_required
def create_post(request):
    template = "posts/create_post.html"
    form = PostForm(request.POST or None, files=request.FILES or None)
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
    form = PostForm(
        request.POST or None, files=request.FILES or None, instance=post
    )
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


@login_required
def add_comment(request, post_id):
    template = "posts:post_detail"
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect(template, post_id=post_id)


@login_required
def follow_index(request):
    template = "posts/follow.html"
    posts = Post.objects.select_related("author").filter(
        author__following__user=request.user
    )
    page_obj = paginate_page(request, posts)
    context = {"page_obj": page_obj}
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    can_following = (
        author != request.user
        and not Follow.objects.filter(
            user=request.user, author=author
        ).exists()
    )
    if can_following:
        Follow.objects.create(user=request.user, author=author)
    return redirect("posts:profile", username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect("posts:profile", username)
