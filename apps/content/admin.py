from hurry.filesize import size

from django.contrib import admin

from .models import Content


class ContentAdmin(admin.ModelAdmin):
    list_display = ('file', 'upload_date', 'size_human', 'content_type', 'url')
    list_filter = ('content_type', 'upload_date')

    def url(self, obj):
        return '<a target="blank" href={0}>{0}</a>'.format(obj.get_absolute_url())
    url.allow_tags = True

    def size_human(self, obj):
        return size(obj.size)


admin.site.register(Content, ContentAdmin)
