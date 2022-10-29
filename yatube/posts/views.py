from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import Post, User
from .models import Group
from .forms import NewPost, CommentForm
from django.core.paginator import Paginator


def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)  # показывать по 10 записей на странице.

    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    return render(
        request,
        'index.html',
        {'page': page, 'paginator': paginator}
    )


# Create your views here.
# view-функция для страницы сообщества
def group_posts(request, slug):
    # функция get_object_or_404 получает по заданным критериям объект из базы данных
    # или возвращает сообщение об ошибке, если объект не найден
    group = get_object_or_404(Group, slug=slug)
    # group = Group.objects
    # Метод .filter позволяет ограничить поиск по критериям. Это аналог добавления
    # условия WHERE group_id = {group_id}
    posts = Post.objects.filter(group=group).order_by("-pub_date")[:12]
    return render(request, "group.html", {'group': group, 'posts': posts})


@login_required
def post_new(request):
    if request.method != 'POST':
        form = NewPost
        return render(request, 'newpost.html', {'form': form})

    form = NewPost(request.POST)

    if not form.is_valid():
        return render(request, 'newpost.html', {'form': form})
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    # по сути происходит перенаправление  url: index из urls.py
    return redirect('index')



def profile(request, username):
    author = get_object_or_404(User, username=username)
    all_posts = Post.objects.all().filter(author__username=username)
    counter = all_posts.count()
    paginator = Paginator(all_posts, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html', {'author': author, 'counter':counter, 'page': page})


def post_view(request, username, post_id):
    # тут тело функции
    author = get_object_or_404(User, username=username)
    all_posts = Post.objects.all().filter(author__username=username)
    post = get_object_or_404(Post, id=post_id)
    counter = all_posts.count()
    form = CommentForm(request.POST or None)
    comments = post.comments.all()
    return render(request, 'post.html',
                  {'author': author,
                   'counter': counter, 'form': form, 'comments': comments,
                   'post': post})


@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    author = get_object_or_404(User, username=username)
    form = NewPost(request.POST or None, files=request.FILES or None,
                   instance=post)

    # if request.method == 'POST':
    if request.user != post.author:
        return redirect('post', username=post.author, post_id=post.id)
    if form.is_valid():
        form.save()
        return redirect('post', username=post.author, post_id=post.id)
    # form = PostForm(instance=post)
    return render(request, 'newpost.html',
                  {'form': form, 'post': post, 'author': author})


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, id=post_id, author__username=username)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
    return redirect('post', username=post.author, post_id=post.id)


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию,
    # выводить её в шаблон пользователской страницы 404 мы не станем
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)