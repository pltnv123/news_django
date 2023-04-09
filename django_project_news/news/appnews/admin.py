from django.contrib import admin
from .models import Post, Comment, Author, Category


class ProductAdmin(admin.ModelAdmin):
    ## list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    # list_display = [field.name for field in
    #                 Product._meta.get_fields()]  # генерируем список имён всех полей для более красивого отображения

    list_display = ('id', 'author', 'categoryType', 'dateCreation', 'title', 'text', 'rating')  # оставляем только имя и цену товара
    list_filter = ('postCategory', 'title', 'rating')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('title', 'category__name')  # тут всё очень похоже на фильтры из запросов в базу


# Register your models here.

admin.site.register(Category)
admin.site.register(Post, ProductAdmin)
admin.site.register(Comment)
admin.site.register(Author)


