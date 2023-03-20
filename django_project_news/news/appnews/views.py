from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse

from news import settings
from .filters import PostFilter
from .forms import PostForm
from .models import *
from datetime import datetime
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class PostNewsList(ListView):
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dateCreation'
    # queryset = Post.objects.order_by(
    #     categoryType_lt='NW',
    # )

    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class PostNewsDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


class PostSearch(ListView):
    form_class = PostForm
    model = Post
    template_name = 'post_search.html'
    context_object_name = 'post_search'
    paginate_by = 10

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('appnews.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        return super().form_valid(form)

    # def form_valid(self, form):
    #     category = form.save(commit=False)
    #     category.categoryType = 'AR'
    #     return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('appnews.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_update')


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('appnews.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('start_new')


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.category).order_by('-dateCreation')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


# Проверка на авторизацию
@login_required()
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)

    if not category.subscribers.filter(id=user.id).exists():
        category.subscribers.add(user)
        # email = user.email
        message = 'Вы успешно подписались на рассылку новостей в категории'

        # msg = EmailMultiAlternatives(
        #     subject=f"Вы успешно подписались на новости из категории {category}.",
        #     body='',
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     to=[email, ]
        # )
        # msg.attach_alternative(html, 'text/html')
        # msg.send
        # return redirect(.....) дописать     html_content =

        return render(request, 'subscribe.html', {'category': category, 'message': message})


@login_required()
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)

    if category.subscribers.filter(id=user.id).exists():
        # email = user.email
        category.subscribers.remove(user)
        message = 'Вы отписались от рассылки новостей в данной категории'

        # msg = EmailMultiAlternatives(
        #     subject=f"Вы отписались от категории {category}.",
        #     body='',
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     to=[email, ],
        # )
        # msg.attach_alternative(html, 'text/html')
        # msg.send
        # return redirect(.....) дописать               # надо еще добавить html_content =

        return render(request, 'unsubscribe.html', {'category': category, 'message': message})


@login_required()
def upgrade_user(request):
    user = request.user
    group = Group.objects.get(name='authors')

    if not user.groups.filter(name='authors').exists():
        group.user_set.add(user)
        Author.objects.create(authorUser=user)
    return redirect('/news')
