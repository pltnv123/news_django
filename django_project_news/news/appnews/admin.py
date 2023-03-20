from django.contrib import admin
from .models import Post, Comment, Author, Category
# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Author)
admin.site.register(Category)
