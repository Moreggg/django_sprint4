from django.contrib import admin

from .models import Category, Comment, Location, Post


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'post',
        'created_at',
        'author'
    )
    readonly_fields = ('created_at',)
    search_fields = ('text', 'post', 'author',)
    list_filter = ('text', 'post', 'author')


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'pub_date',
        'created_at',
        'author',
        'location',
        'category',
        'is_published',
    )
    list_editable = (
        'is_published',
    )
    readonly_fields = ('created_at',)
    search_fields = ('title', 'text', 'location__name')
    list_filter = ('category', 'location')
    empty_value_display = 'Планета земля'


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'created_at',
        'is_published',
    )
    list_editable = (
        'is_published',
    )
    search_fields = ('name',)
    readonly_fields = ('created_at',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'created_at',
        'description',
        'slug',
        'is_published',
    )
    search_fields = ('title',)
    list_editable = ('is_published',)
    readonly_fields = ('created_at',)


admin.site.register(Post, PostAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
