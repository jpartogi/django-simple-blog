from django.contrib import admin

from django.contrib.auth.models import User
from simple_blog.models import *

class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'timezone')

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'description', 'slug')

class EntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'posted'
    list_select_related = True
    search_fields = ('title', 'content')
    exclude = ('creator', 'created')
    list_display = ('title', 'category', 'creator', 'posted', 'created', 'updated', 'is_draft')
    list_filter = ('created', 'category')
    prepopulated_fields = {"slug": ("title",)}

    def save_model(self, request, obj, form, change):
        if change != True:
            obj.creator = User.objects.get(username=request.user.username)
        obj.save()

admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Entry, EntryAdmin)