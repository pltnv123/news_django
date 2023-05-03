from django.core.cache import cache
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy

class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0, help_text=gettext_lazy('Рейтинг автора'))

    def update_rating(self):
        """ Обновляет рейтинг текущего автора.
            Суммарный рейтинг каждой статьи автора умножается на 3;
            Суммарный рейтинг всех комментариев автора;
            Суммарный рейтинг всех комментариев к статьям автора. """

        # к модели post связанной, применяем функцию
        # .aggregate   которая применяет функцию Sum к полю rating
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        # обращаемся к красной postRating выше на две строки
        pRat += postRat.get('postRating')
        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()

    def __str__(self):
        return self.authorUser.username


class Category(models.Model):
    """   Категории новостей/статей   """

    name = models.CharField(max_length=128, unique=True, help_text=gettext_lazy('Имя категории'))
    subscribers = models.ManyToManyField(User, related_name='categories', blank=True)

    def __str__(self):
        return self.name.title()


class Post(models.Model):

    """   Содержит в себе статьи и новости, которые создают пользователи, у одного поста,
          может быть несколько категорий    """

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOIESES = (
        (NEWS, gettext_lazy('Новость')),
        (ARTICLE, gettext_lazy('Статья'))
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOIESES, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField('Category', through='PostCategory')
    title = models.CharField(max_length=128, help_text=gettext_lazy('Название поста'))
    text = models.TextField(help_text=gettext_lazy('Это текст поста'))
    rating = models.SmallIntegerField(default=0, help_text=gettext_lazy('Рейтинг поста'))

    # Метод preview() модели Post, который возвращает начало статьи
    # (предварительный просмотр) длиной 124 символа и добавляет многоточие в конце.
    def preview(self):
        return self.text[0:124] + '...'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f' {self.title} '

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id), ])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')

    class Meta:
        verbose_name = gettext_lazy('Пост')
        verbose_name_plural = gettext_lazy('Посты')


class PostCategory(models.Model):
    """   Промежуточная модель для связи «многие ко многим с моделью Post и Category   """

    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    """   Комментарии под посты и статьи   """

    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.commentUser} |  {self.text}'
