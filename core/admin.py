# Register your models here.
from django.contrib import admin
from core.models import Expose, ExposeUser
from django.db import models
from django_json_widget.widgets import JSONEditorWidget


class ExposeAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "file", "created_at", "updated_at")
    date_hierarchy = "created_at"
    list_filter = ("status",)
    search_fields = (
        "status",
        "file",
    )
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }


class ExposeUserAdmin(admin.ModelAdmin):
    list_display = ("expose", "user", "created_at", "updated_at")
    date_hierarchy = "created_at"
    list_filter = ("expose",)
    search_fields = (
        "expose",
        "user",
    )


admin.site.register(Expose, ExposeAdmin)

admin.site.register(ExposeUser, ExposeUserAdmin)
