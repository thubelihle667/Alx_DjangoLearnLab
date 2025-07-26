from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Book

# Book Admin
class BookAdmin(admin.ModelAdmin):
    list_filter = ("title", "author", "publication_year")
    search_fields = ("title", "author", "publication_year")

admin.site.register(Book, BookAdmin)

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo',)}),
    )

    list_display = UserAdmin.list_display + ('date_of_birth', 'profile_photo',)
    search_fields = UserAdmin.search_fields + ('date_of_birth',)
    list_filter = UserAdmin.list_filter + ('date_of_birth',)

admin.site.register(CustomUser, CustomUserAdmin)
