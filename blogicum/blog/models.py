from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from . import const

User = get_user_model()


class CreatedAtModel(models.Model):
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('created_at',)


class IsPublishedCreateAtModel(CreatedAtModel):
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )

    class Meta:
        abstract = True


class Location(IsPublishedCreateAtModel):
    name = models.CharField('Название места', max_length=const.MAX_LENGTH)

    class Meta(CreatedAtModel.Meta):
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name[:const.OBJ_STR_SLICE]


class Category(IsPublishedCreateAtModel):
    title = models.CharField('Заголовок', max_length=const.MAX_LENGTH)
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text=('Идентификатор страницы для URL; '
                   'разрешены символы латиницы, цифры, '
                   'дефис и подчёркивание.')
    )

    class Meta(CreatedAtModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:const.OBJ_STR_SLICE]


class Post(IsPublishedCreateAtModel):
    title = models.CharField('Заголовок', max_length=const.MAX_LENGTH)
    text = models.TextField('Текст',)
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text='Если установить дату и время в будущем — можно '
                  'делать отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
    )
    image = models.ImageField('Фото', upload_to='post_images', blank=True)

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        default_related_name = 'posts'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title[:const.OBJ_STR_SLICE]

    def get_absolute_url(self):
        return reverse(
            'blog:profile',
            kwargs={"username": self.author.username}
        )


class Comment(CreatedAtModel):
    text = models.TextField('Текст комментария')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Публикация'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )

    class Meta(CreatedAtModel.Meta):
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.post_id})

    def __str__(self):
        return self.text[:const.OBJ_STR_SLICE]
