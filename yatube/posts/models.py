from django.db import models
from django.contrib.auth import get_user_model

# В проекте Yatube мы дадим пользователям возможность регистрироваться и создавать свои страницы,
# и нам нужен инструмент для создания и администрирования аккаунтов. В Django встроена работа с пользователями.
# Для управления ими создана специальная модель User, и мы импортируем её.
# Официальная документация рекомендует обращаться к модели User через функцию get_user_model. Следуем этой рекомендации:


User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=309)
    # используется для записи url адресов
    slug = models.SlugField(max_length=160, unique=True)
    description = models.TextField(max_length=300)

    def __str__(self):
        return self.title


# Обратите внимание на поле author. Оно ссылается на автора поста, на модель User,
# и для этого поля указано свойство related_name="posts".
# Тут снова начинается магия: в каждом объекте модели User автоматически будет создано свойство с таким же названием (posts),
# и в нём будут храниться ссылки на все объекты модели Post, которые ссылаются на объект User.
# На практике это означает, что в объекте записи есть поле author, в котором хранится ссылка на автора(например, admin),
# а в объекте пользователя admin появилось поле posts, в котором хранятся ссылки на все посты этого автора.
# И теперь можно получить список постов автора, обратившись к его свойству posts

class Post(models.Model):
    # класс Post, наследник класса Model из библиотеки models
    # свойство text типа TextField
    text = models.TextField()

    pub_date = models.DateTimeField("date published", auto_now_add=True)
    # свойство author типа ForeignKey, ссылка на модель User
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    # прочитать как это работает
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, related_name="posts", blank=True, null=True)
    # поле для картинки
    # Аргумент upload_to указывает, куда должны загружаться пользовательские файлы.
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField("Дата публикации", auto_now_add=True)

    def __str__(self):
        return self.text


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower',
                             verbose_name='Пользователь подписан на')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following', verbose_name='Автора')
