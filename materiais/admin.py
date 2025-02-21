from django.contrib import admin
from .models import Material

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('nome', 'curso', 'tipo', 'ativo', 'created_at', 'updated_at')
    list_filter = ('ativo', 'tipo', 'curso', 'created_at')
    search_fields = ('nome', 'descricao', 'curso__nome')
