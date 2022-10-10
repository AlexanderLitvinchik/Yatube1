from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import Post
from .models import Group
from .forms import PostForm

def index(request):
    # одна строка вместо тысячи слов на SQL, берем первые 10 строк взятые отсорченые по дате с конца
    latest = Post.objects.order_by('-pub_date')[:10]
    # # собираем тексты постов в один, разделяя новой строкой
    # output = []
    # for item in latest:
    #     output.append(item.text)
    # return HttpResponse('\n'.join(output))
    return render(request, "index.html", {"posts": latest})


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
    return render(request, "group.html", {"group": group, "posts": posts})


@login_required
def post_new(request):
    if request.method != 'POST':
        form = PostForm()
        return render(request, 'newpost.html', {'form': form})

    form = PostForm(request.POST)

    if not form.is_valid():
        return render(request, 'newpost.html', {'form': form})
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect('index')
