from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from blog.models import BlogPost

# Список статей (только опубликованные)
class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        """Фильтрация: только опубликованные статьи"""
        return BlogPost.objects.filter(is_published=True).order_by('-created_at')


# Детальная страница (с увеличением просмотров)
class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        """Переопределяем get_object, чтобы увеличить счётчик просмотров"""
        obj = super().get_object(queryset=queryset)
        obj.views_count += 1
        obj.save(update_fields=['views_count'])
        return obj


# Создание записи
class BlogPostCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = BlogPost
    fields = ['title', 'content', 'preview', 'is_published']
    template_name = 'blog/blogpost_form.html'
    success_url = reverse_lazy('blog:list')
    permission_required = 'blog.add_blogpost'


# Редактирование записи
class BlogPostUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = BlogPost
    fields = ['title', 'content', 'preview', 'is_published']
    template_name = 'blog/blogpost_form.html'
    permission_required = 'blog.change_blogpost'

    def get_success_url(self):
        """После редактирования перенаправляем на детальную страницу этой записи"""
        return reverse_lazy('blog:detail', kwargs={'pk': self.object.pk})


# Удаление записи
class BlogPostDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = BlogPost
    template_name = 'blog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blog:list')
    permission_required = 'blog.delete_blogpost'
