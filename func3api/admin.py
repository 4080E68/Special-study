from django.contrib import admin

from func3api.models import *

admin.site.register(Location)


class displayAdmin(admin.ModelAdmin):
    list_display=('id','name','price','commodity','url_list','pc_images')
    list_filter = ('name','price')
    search_fields = ('name',)
    ordering=('id',)

admin.site.register(display,displayAdmin)
