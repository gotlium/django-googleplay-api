# -*- coding: utf-8 -*-

from django.contrib import admin

from preferences.admin import PreferencesAdmin

from .models import GooglePlayPreferences


class PreferencesAdmin(PreferencesAdmin):
    exclude = ('sites',)

    def add_view(self, *args, **kwargs):
        return self.changelist_view(*args, **kwargs)

    def has_add_permission(self, request):
        return False

    class Media:
        js = (
            '/static/djgpa/admin/js/djgpa.js',
        )


admin.site.register(GooglePlayPreferences, PreferencesAdmin)
