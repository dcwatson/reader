from django.contrib import admin

from .models import User


class UserAdmin (admin.ModelAdmin):
    list_display = ('email', 'name', 'is_active', 'is_admin', 'last_login')
    list_filter = ('is_active', 'is_admin')


admin.site.register(User, UserAdmin)
