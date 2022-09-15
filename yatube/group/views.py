from django.shortcuts import render, get_object_or_404
from group.models import Group, Group1
from posts.models import Post

# Create your views here.
# view-функция для страницы сообщества
def group_posts(request, slug):
    # функция get_object_or_404 получает по заданным критериям объект из базы данных
    # или возвращает сообщение об ошибке, если объект не найден
    group = get_object_or_404(Group1)
    #group = Group.objects
    # Метод .filter позволяет ограничить поиск по критериям. Это аналог добавления
    # условия WHERE group_id = {group_id}
    posts = Post.objects.order_by("-pub_date")[:12]
    return render(request, "group.html", {"group": group, "posts": posts})
