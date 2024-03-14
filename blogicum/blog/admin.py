from django.contrib import admin

from .models import Category, Location, Post


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
