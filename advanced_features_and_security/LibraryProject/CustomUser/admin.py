from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo',)}),
    )

    list_display = UserAdmin.list_display + ('date_of_birth', 'profile_photo',)
    search_fields = UserAdmin.search_fields + ('date_of_birth', 'profile_photo',)
    list_filter = UserAdmin.list_filter + ('date_of_birth', 'profile_photo',)

#admin.site.register(CustomUser, UserAdmin)