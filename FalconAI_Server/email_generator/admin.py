from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import AIEmail, Business, Campaign, Employee, EmployeeAction, FlaconAIUser


class UserAdmin(BaseUserAdmin):
    list_display = ("email", "first_name", "last_name")
    list_filter = ("is_admin",)
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    filter_horizontal = ()


admin.site.register(FlaconAIUser, UserAdmin)
admin.site.register(Business)
admin.site.register(Employee)
admin.site.register(Campaign)
admin.site.register(AIEmail)
admin.site.register(EmployeeAction)
