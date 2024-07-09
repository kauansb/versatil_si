from django.contrib import admin
from materiais.models import Material


class MaterialAdmin(admin.ModelAdmin):
    list_display = ('curso','nome','descricao','arquivo')
    search_fields = ('nome',)

admin.site.register(Material, MaterialAdmin)
