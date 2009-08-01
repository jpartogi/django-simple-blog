from datetime import datetime

from django.contrib import admin

from django.contrib.auth.models import User
from djblog.models import *
"""
class BlogAdmin(admin.ModelAdmin):
    pass
"""
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'description']

class EntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'posted'
    list_select_related = True
    search_fields = ('title', 'content')
    exclude = ('creator', 'created')
    list_display = ('title', 'category', 'creator', 'posted', 'created', 'is_draft')
    list_filter = ('posted', 'created', 'category')
    prepopulated_fields = {"slug": ("title",)}

    def save_model(self, request, obj, form, change):
        obj.creator = User.objects.get(username=request.user.username)
        obj.save()

#admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Entry, EntryAdmin)