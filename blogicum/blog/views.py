from django.db.models import Count
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.timezone import now
from django.views.generic import UpdateView, ListView, CreateView, DeleteView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from . import service

from .models import Category, Post
from . import const
from .forms import CommentForm, PostForm
from .mixins import CommentMixin, OnlyAuthorMixin


def select_post(postmanager):
    return postmanager.select_related(
        'author',
        'location',
        'category',
    ).annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date',)


def filter_post(queryset):
    return queryset.filter(
        pub_date__lt=now(),
        is_published=True,
        category__is_published=True
    )


def profile(request, username):
    author = get_object_or_404(get_user_model(), username=username)
    posts = select_post(Post.objects).filter(author__exact=author.id)
    if request.user != author:
        posts = filter_post(posts)
    page_obj = service.paginate(request, posts)
    return render(
        request,
        'blog/profile.html',
        {'profile': author, 'page_obj': page_obj}
    )


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = filter_post(select_post(category.posts))
    page_obj = service.paginate(request, posts)
    return render(
        request,
        'blog/category.html',
        {'page_obj': page_obj, 'category': category}
    )


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        post = get_object_or_404(filter_post(Post.objects), pk=post_id)
    return render(
        request,
        'blog/detail.html',
        {
            'post': post,
            'form': CommentForm(),
            'comments': post.comments.select_related('author')
        }
    )


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', post_id=post_id)


def delete_post(request, post_id):
    instance = get_object_or_404(Post, pk=post_id)
    if request.user != instance.author:
        return redirect('blog:post_detail', post_id=post_id)
    form = PostForm(instance=instance)
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/create.html', {'form': form})


class DeleteCommentView(CommentMixin, OnlyAuthorMixin, DeleteView):
    pass


class EditPostView(OnlyAuthorMixin, UpdateView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'
    form_class = PostForm

    def handle_no_permission(self):
        return redirect(reverse(
            'blog:post_detail', kwargs={"post_id": self.kwargs.get('post_id')})
        )

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.object.id})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class EditCommentView(CommentMixin, OnlyAuthorMixin, UpdateView):
    pass


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    fields = ('first_name', 'last_name', 'username', 'email')
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse("blog:profile",
                       kwargs={"username": self.object.username})


class IndexView(ListView):
    template_name = 'blog/index.html'
    model = Post
    queryset = filter_post(select_post(Post.objects))
    paginate_by = const.POSTS_ON_PAGE
