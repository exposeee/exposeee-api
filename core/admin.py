# Register your models here.
from django.contrib import admin
from core.models import Expose, ExposeUser


class ExposeAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'file', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    list_filter = ('status', 'user')
    search_fields = (
        'status', 'file',
    )


class ExposeUserAdmin(admin.ModelAdmin):
    list_display = ('expose', 'user', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    list_filter = ('expose',)
    search_fields = (
        'expose', 'user',
    )


admin.site.register(Expose, ExposeAdmin)

admin.site.register(ExposeUser, ExposeUserAdmin)
