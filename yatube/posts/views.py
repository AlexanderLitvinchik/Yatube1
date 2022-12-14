from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Post, Group, User, Follow
from .forms import NewPost, CommentForm
from django.shortcuts import redirect
from http import HTTPStatus


def index(request):
    latest = Post.objects.all()
    paginator = Paginator(latest, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'group.html',
                  {'group': group, 'posts': posts, 'page': page})


@login_required
def post_new(request):
    if request.method != 'POST':
        form = NewPost()
        return render(request, 'newpost.html', {'form': form})

    form = NewPost(request.POST)

    if not form.is_valid():
        return render(request, 'newpost.html', {'form': form})
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect('index')


def profile(request, username):
    author = get_object_or_404(User, username=username)
    all_posts = Post.objects.all().filter(author__username=username)
    counter = all_posts.count()
    following = author.following.all()
    follower = author.follower.all()
    count_follower = follower.count()
    count_following = following.count()
    paginator = Paginator(all_posts, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html',
                  {'page': page,
                   'author': author,
                   'counter': counter,
                   'count_following': count_following,
                   'count_follower': count_follower,
                   'following': following})


def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)
    full_post = get_object_or_404(Post, id=post_id)
    post = get_object_or_404(Post, id=post_id)
    all_posts = Post.objects.all().filter(author__username=username)
    following = author.following.all()
    follower = author.follower.all()
    count_follower = follower.count()
    count_following = following.count()
    counter = all_posts.count()
    form = CommentForm(request.POST or None)
    comments = post.comments.all()
    return render(request, 'post.html',
                  {'author': author,
                   'counter': counter,
                   'form': form,
                   'comments': comments,
                   'post': post,
                   'full_post': full_post,
                   'count_follower': count_follower,
                   'count_following': count_following})


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, id=post_id, author__username=username)
    form = CommentForm(request.POST or None)

    if not form.is_valid():
        return redirect('post', username=post.author.username, post_id=post_id)
    comment = form.save(commit=False)
    comment.post = post
    comment.author = request.user
    comment.save()
    return redirect('post', username=post.author, post_id=post.id)


@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    author = get_object_or_404(User, username=username)
    form = NewPost(request.POST or None, files=request.FILES or None,
                    instance=post)

    if request.user != post.author:
        return redirect('post', username=post.author, post_id=post.id)
    if form.is_valid():
        form.save()
        return redirect('post', username=post.author, post_id=post.id)
    return render(request, 'newpost.html',
                  {'form': form, 'post': post, 'author': author})


def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=HTTPStatus.NOT_FOUND
    )


def server_error(request):
    return render(request, 'misc/500.html', status=500)


@login_required
def follow_index(request):
    post_list_follow = Post.objects.filter(
        author__following__user=request.user)
    paginator = Paginator(post_list_follow, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'follow.html',
                  {'page': page, 'paginator': paginator})


@login_required
def profile_follow(request, username):
    follow = get_object_or_404(User, username=username)
    already = Follow.objects.filter(user=request.user, author=follow).exists()

    if request.user.username == username:
        return redirect('profile', username=username)

    if not already:
        Follow.objects.get_or_create(user=request.user, author=follow)
    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    following = get_object_or_404(User, username=username)
    follower = get_object_or_404(Follow, author=following, user=request.user)
    follower.delete()
    return redirect('profile', username=username)
