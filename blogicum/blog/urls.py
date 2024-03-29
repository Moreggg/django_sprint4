from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('',
         views.IndexView.as_view(),
         name='index'),
    path('posts/create/',
         views.PostCreateView.as_view(),
         name='create_post'),
    path('posts/<int:post_id>/',
         views.post_detail,
         name='post_detail'),
    path('posts/<int:post_id>/edit/',
         views.EditPostView.as_view(),
         name='edit_post'),
    path('posts/<int:post_id>/delete/',
         views.delete_post,
         name='delete_post'),
    path('posts/<int:post_id>/comment/',
         views.add_comment,
         name='add_comment'),
    path('posts/<int:post_id>/edit_comment/<int:comment_id>/',
         views.EditCommentView.as_view(),
         name='edit_comment'),
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/',
         views.DeleteCommentView.as_view(),
         name='delete_comment'),
    path('profile/<str:username>/',
         views.profile,
         name='profile'),
    path('edit_profile/',
         views.EditProfileView.as_view(),
         name='edit_profile'),
    path('category/<slug:category_slug>/',
         views.category_posts,
         name='category_posts')
]
