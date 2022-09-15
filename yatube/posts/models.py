from django.db import models
from django.contrib.auth import get_user_model
from group.models import Group

# В проекте Yatube мы дадим пользователям возможность регистрироваться и создавать свои страницы,
# и нам нужен инструмент для создания и администрирования аккаунтов. В Django встроена работа с пользователями.
# Для управления ими создана специальная модель User, и мы импортируем её.
# Официальная документация рекомендует обращаться к модели User через функцию get_user_model. Следуем этой рекомендации:


User = get_user_model()


# Обратите внимание на поле author. Оно ссылается на автора поста, на модель User,
# и для этого поля указано свойство related_name="posts".

# Насколько я понял где-то не видемо для нас создастся модель User для каждого объекта и там будут
# хранится посты данного пользователя

# Тут снова начинается магия: в каждом объекте модели User автоматически будет создано свойство с таким же названием (posts),
# и в нём будут храниться ссылки на все объекты модели Post, которые ссылаются на объект User.
# На практике это означает, что в объекте записи есть поле author, в котором хранится ссылка на автора(например, admin),
# а в объекте пользователя admin появилось поле posts, в котором хранятся ссылки на все посты этого автора.
# И теперь можно получить список постов автора, обратившись к его свойству posts

# Свойства модели связаны со столбцами таблицы в БД, а методы превращаются в запросы.
# Для свойств моделей указывают типы данных, соответствующие типам данных в БД.
# Параметр on_delete=models.CASCADE обеспечивает связность данных:
# если из таблицы User будет удалён пользователь, то будут удалены все связанные с ним посты.

class Post(models.Model):
    # класс Post, наследник класса Model из библиотеки models
    # свойство text типа TextField
    text = models.TextField()

    # свойство pub_date типа DateTimeField, текст "date published" это заголовок
    # поля в интерфейсе администратора. auto_now_add говорит, что при создании
    # новой записи автоматически будет подставлено текущее время и дата
    pub_date = models.DateTimeField("date published", auto_now_add=True)

    # свойство author типа ForeignKey, ссылка на модель User
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    # прочитать как это работает
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, related_name="posts", blank=True, null=True)
