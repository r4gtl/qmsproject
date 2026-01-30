from django.contrib import admin
from .models import Company, Profile


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'subscription_plan', 'created_at']
    list_filter = ['is_active', 'subscription_plan', 'created_at']
    search_fields = ['name', 'slug', 'vat_number']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Informazioni Azienda', {
            'fields': ('name', 'slug', 'vat_number')
        }),
        ('Indirizzo', {
            'fields': ('address', 'city', 'country')
        }),
        ('Branding', {
            'fields': ('logo',)
        }),
        ('Subscription', {
            'fields': ('is_active', 'subscription_plan', 'subscription_expires')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'role', 'created_at']
    list_filter = ['role', 'company', 'created_at']
    search_fields = ['user__username', 'user__email', 'company__name']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('User & Company', {
            'fields': ('user', 'company', 'role')
        }),
        ('Profile Info', {
            'fields': ('avatar', 'bio', 'phone', 'department')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
