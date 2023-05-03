from django.contrib import admin
from .models import Post, Comment, Author, Category
from modeltranslation.admin import TranslationAdmin
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'categoryType', 'dateCreation', 'title', 'text', 'rating')
    list_filter = ('author', 'postCategory', 'title', 'rating')
    search_fields = ('title__icontains', 'postCategory__name__icontains')




class CategoryAdmin(TranslationAdmin):
    model = Category


class PostAdmin(TranslationAdmin):
    model = Post


# Register your models here.

admin.site.register(Category)
admin.site.register(Post, ProductAdmin)
admin.site.register(Comment)
admin.site.register(Author)
