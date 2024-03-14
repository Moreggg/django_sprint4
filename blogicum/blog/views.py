from django.db.models.base import Model as Model
from django.db.models import Count
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.timezone import now
from django.views.generic import UpdateView, ListView, CreateView, DeleteView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseForbidden

from .models import Category, Post, Comment
from . import const
from .forms import CommentForm, PostForm


def profile(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    if request.user.username == username:
        post_list = Post.objects.select_related(
            'author', 'location', 'category',
        ).filter(
            author__exact=user.id
        ).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date',)
    else:
        post_list = filter_pub_post(Post.objects).filter(author__exact=user.id)
    paginator = Paginator(post_list, const.POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'blog/profile.html',
        {'profile': user, 'page_obj': page_obj}
    )


def filter_pub_post(postmanager):
    return postmanager.select_related(
        'author',
        'location',
        'category',
    ).filter(
        pub_date__lt=now(),
        is_published=True,
        category__is_published=True
    ).annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date',)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = filter_pub_post(category.posts)
    paginator = Paginator(post_list, const.POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'blog/category.html',
        {'page_obj': page_obj, 'category': category}
    )


def post_detail(request, post_id):
    if request.user.id == get_object_or_404(Post, pk=post_id).author_id:
        post = get_object_or_404(Post, pk=post_id)
    else:
        post = get_object_or_404(
            filter_pub_post(Post.objects),
            pk=post_id,
        )
    comments = Comment.objects.filter(post_id=post_id).select_related('author')
    form = CommentForm()
    return render(
        request,
        'blog/detail.html',
        {
            'post': post,
            'form': form,
            'comments': comments
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
    form = PostForm(instance=instance)
    if request.user.id != Post.objects.get(pk=post_id).author_id:
        return HttpResponseForbidden()
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:index')
    return render(request, 'blog/create.html', {'form': form})


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author_id == self.request.user.id


class DeleteCommentView(OnlyAuthorMixin, DeleteView):
    model = Comment
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'
    success_url = reverse_lazy('blog:index')


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
        return reverse("blog:post_detail", kwargs={"post_id": self.object.id})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class EditCommentView(OnlyAuthorMixin, UpdateView):
    model = Comment
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'
    form_class = CommentForm


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    fields = ['first_name', 'last_name', 'username', 'email']
    template_name = 'blog/user.html'
    success_url = reverse_lazy('blog:profile')

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse("blog:profile",
                       kwargs={"username": self.object.username})


class IndexView(ListView):
    template_name = 'blog/index.html'
    model = Post
    queryset = filter_pub_post(Post.objects)
    paginate_by = const.POSTS_ON_PAGE
