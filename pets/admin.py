from django.contrib import admin

from django.contrib import admin
from .models import User, Animal, AdoptionRequest
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Extra info', {'fields': ('is_admin',)}),
    )
    list_display = ('username', 'email', 'is_staff', 'is_admin')

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'age', 'adopted', 'created_at')
    list_filter = ('species', 'adopted')
    search_fields = ('name',)

@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ('animal', 'user', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('animal__name', 'user__username')
