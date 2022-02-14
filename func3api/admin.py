from django.contrib import admin

from func3api.models import *


class cpuAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'commodity',
                    'vendor')
    list_filter = ('name', 'price')
    search_fields = ('name',)
    ordering = ('id',)

class displayAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'commodity',
                     'vendor')
    list_filter = ('name','price')
    search_fields = ('name',)
    ordering=('id',)


class ssdAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'commodity',
                     'vendor')
    list_filter = ('name', 'price')
    search_fields = ('name',)
    ordering = ('id',)

admin.site.register(display,displayAdmin)
admin.site.register(cpu, cpuAdmin)
admin.site.register(ssd, ssdAdmin)
