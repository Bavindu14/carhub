
from django.contrib import admin
from .models import Car
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'year')
    list_filter = ('brand', 'year')
    search_fields = ('title', 'brand__name')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)



