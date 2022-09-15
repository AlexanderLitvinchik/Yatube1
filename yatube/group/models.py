from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

# читать коммент в файле posts.models здесь для каждой группы будут зранится посты
Group1 = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=309)
    # используется для записи url адресов
    slug = models.SlugField(unique=True)

    description = models.TextField(max_length=300)

    def __str__(self):
        return self.title
