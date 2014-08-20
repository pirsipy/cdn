from django.contrib import admin
from django.contrib.auth.models import Group

from authtools.admin import NamedUserAdmin, BASE_FIELDS, SIMPLE_PERMISSION_FIELDS, DATE_FIELDS

from .models import User


class UserAdmin(NamedUserAdmin):
    fieldsets = (
        BASE_FIELDS,
        SIMPLE_PERMISSION_FIELDS,
        DATE_FIELDS)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
