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
class BlogPostCreateView(CreateView):
    model = BlogPost
    fields = ['title', 'content', 'preview', 'is_published']
    template_name = 'blog/blogpost_form.html'
    success_url = reverse_lazy('blog:list')


# Редактирование записи
class BlogPostUpdateView(UpdateView):
    model = BlogPost
    fields = ['title', 'content', 'preview', 'is_published']
    template_name = 'blog/blogpost_form.html'

    def get_success_url(self):
        """После редактирования перенаправляем на детальную страницу этой записи"""
        return reverse_lazy('blog:detail', kwargs={'pk': self.object.pk})


# Удаление записи
class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blog:list')
