from datetime import datetime

from django.contrib import admin

from portal.apps.member.models import Member
from portal.apps.blog.models import Entry

class EntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'posted'
    list_select_related = True
    search_fields = ('title', 'content')
    exclude = ('creator', 'created')
    list_display = ('title', 'category', 'creator', 'posted', 'created')
    list_filter = ('posted', 'created', 'category')
    prepopulated_fields = {"slug": ("title",)}

    def save_model(self, request, obj, form, change):
        obj.creator = Member.objects.get(username=request.user.username)
        obj.created = datetime.now()

        obj.save()

admin.site.register(Entry, EntryAdmin)