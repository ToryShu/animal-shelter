from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import AdoptionRequest, Animal, ShelterSettings, User

@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ('animal', 'user', 'status', 'created_at', 'actions_buttons')
    list_filter = ('status',)
    search_fields = ('animal__name', 'user__username')
    actions = None

    def actions_buttons(self, obj):
        if obj.status == 'pending':
            return format_html(
                '<a class="button" href="approve/{0}">Approve</a>&nbsp;'
                '<a class="button" href="reject/{0}">Reject</a>',
                obj.id
            )
        return '-'
    actions_buttons.short_description = 'Actions'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('approve/<int:adoption_id>/', self.admin_site.admin_view(self.approve_adoption)),
            path('reject/<int:adoption_id>/', self.admin_site.admin_view(self.reject_adoption)),
        ]
        return custom_urls + urls

    def approve_adoption(self, request, adoption_id):
        adoption = AdoptionRequest.objects.get(id=adoption_id)
        adoption.status = 'approved'
        adoption.save()
        self.message_user(request, f"Adoption request {adoption_id} approved.")
        return redirect(request.META.get('HTTP_REFERER'))

    def reject_adoption(self, request, adoption_id):
        adoption = AdoptionRequest.objects.get(id=adoption_id)
        adoption.status = 'rejected'
        adoption.save()
        self.message_user(request, f"Adoption request {adoption_id} rejected.")
        return redirect(request.META.get('HTTP_REFERER'))

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

@admin.register(ShelterSettings)
class ShelterSettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address') 
