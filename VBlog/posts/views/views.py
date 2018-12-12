from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from posts.models import Post
from posts.forms.post_form import PostModelForm
from django.db.models import Q
from django.template.defaultfilters import slugify


# Function based - List View
# def posts_list(request):
#     posts = Post.objects.filter(draft=False)
#     query = request.GET.get('q')
#     if query:
#         posts = posts.filter(
#             Q(title__icontains=query) |
#             Q(content__icontains=query) |
#             Q(user__first_name__icontains=query) |
#             Q(user__last_name__icontains=query)
#         ).distinct()
#     paginator = Paginator(posts, 5)
#     page = request.GET.get('page')
#     try:
#         page_posts = paginator.get_page(page)
#     except PageNotAnInteger:
#         page_posts = paginator.page(1)
#     except EmptyPage:
#         page_posts = paginator.page(paginator.num_pages)
#
#     context = {'posts': page_posts}
#     return render(request=request, template_name='posts/list.html', context=context)


class PostListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Post
    context_object_name = 'posts'
    template_name = 'posts/list.html'
    paginate_by = 5

    def get_queryset(self, **kwargs):
        query = self.request.GET.get("q")
        qs = Post.objects.filter(draft=False).order_by('-timestamp')
        if query:
            qs = Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            ).distinct()
        return qs


class MyPostListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Post
    context_object_name = 'posts'
    template_name = 'posts/list.html'
    paginate_by = 5

    def get_queryset(self, **kwargs):
        query = self.request.GET.get("q")
        qs = Post.objects.filter(user=self.request.user).order_by('-timestamp')
        if query:
            qs = Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            ).distinct()
        return qs

    # def get_context_data(self, **kwargs):
    #     query = self.request.GET.get("q")
    #     qs = Post.objects.filter(draft=False)
    #     if query:
    #         qs = Post.objects.filter(
    #             Q(title__icontains=query) |
    #             Q(content__icontains=query) |
    #             Q(user__first_name__icontains=query) |
    #             Q(user__last_name__icontains=query)
    #         ).distinct()
    #     context = super(PostListView, self).get_context_data(**kwargs)
    #     context["posts"] = qs
    #     return context


# Function based - Create View
# def posts_create(request):
#     form = CreatePost(request.POST or None, request.FILES or None)
#     if form.is_valid():
#         instance = form.save(commit=False)
#         instance.user = request.user
#         instance.save()
#         messages.success(request, "The blog has been created successfully!")
#         return redirect(instance.get_absolute_url())
#     context = {
#         "form": form,
#     }
#     return render(request, "posts/create.html", context)


class PostCreateView(SuccessMessageMixin,LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = Post
    template_name = 'posts/create.html'
    form_class = PostModelForm
    queryset = Post.objects.filter(draft=False)
    success_url = '/posts/'
    success_message = "'%(title)s' blog has been created successfully!"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

# Function based - Detail View
# def posts_detail(request, slug=None):
#     post = Post.objects.get(slug=slug)
#     return render(request, 'posts/detail.html', {'post': post})


class PostDetailView(LoginRequiredMixin, DetailView):
    login_url = 'login'
    model = Post
    template_name = 'posts/detail.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Post, **self.kwargs)


# Function based - Update View
# def posts_update(request, slug=None):
#     instance = Post.objects.get(slug=slug)
#     form = CreatePost(request.POST or None, request.FILES or None, instance=instance)
#     if form.is_valid():
#         instance = form.save(commit=False)
#         instance.user = request.user
#         instance.save()
#         messages.success(request, "The blog has been updated successfully!")
#         return redirect(instance.get_absolute_url())
#     context = {
#         "form": form,
#     }
#     return render(request, "posts/create.html", context)


class PostUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = Post
    template_name = 'posts/edit.html'
    form_class = PostModelForm
    success_url = reverse_lazy('posts:list')
    success_message = "'%(title)s' has been updated successfully!"

    def get_object(self, queryset=None):
        return get_object_or_404(Post, **self.kwargs)

    def form_valid(self, form):
        return super().form_valid(form)


# Function based - Delete View
# def posts_delete(request, slug=None):
#     post = Post.objects.get(slug=slug)
#     post.delete()
#     messages.success(request, "The blog has been deleted successfully!")
#     return redirect('posts:list')


class PostDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = Post
    success_url = '/posts/'

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, **self.kwargs)
        messages.success(self.request, "'{}' has been deleted successfully".format(post.title.title()))
        return post
