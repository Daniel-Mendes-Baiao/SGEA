from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'user', 'action', 'target_model', 'target_id']
    list_filter = ['action', 'target_model', 'timestamp']
    search_fields = ['user__username', 'action', 'details']
    readonly_fields = ['user', 'action', 'target_model', 'target_id', 'details', 'timestamp']
    ordering = ['-timestamp']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
