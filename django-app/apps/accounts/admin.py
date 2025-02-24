from django.contrib import admin

from . import models


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
    )


admin.site.register(models.CustomUser, CustomUserAdmin)
