from django.contrib import admin

from .models import Group

#
# class ArticalAdmin(admin.ModelAdmin):
#     prepopulated_fields = {"slug": ("title",)}


class GroupAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "slug", "description")
    # добавляем интерфейс для поиска по тексту постов
    search_fields = ("title",)
    # добавляем возможность фильтрации по дате
    empty_value_display = "-пусто-"
    # это свойство сработает для всех колонок: где пусто - там будет эта строка


admin.site.register(Group, GroupAdmin)
