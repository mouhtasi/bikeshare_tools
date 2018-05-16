from django.contrib import admin
from bikesharestationcatalog.models import StationImage
from django.utils.html import format_html


@admin.register(StationImage)
class StationImageAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        return format_html(
            '<a href="{}"><img src="{}" style="max-width: 400px; max-height: 400px"/></a>'.format(obj.image.url,
                                                                                                  obj.image.url))

    image_tag.short_description = 'Image'

    list_display = ('station', 'image_tag', 'approved')
    fields = ('station', 'date', 'image_tag', 'approved')
    readonly_fields = ('date', 'image_tag')
