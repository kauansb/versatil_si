import csv
from django.contrib import admin
from django.http import HttpResponse
from matriculas.models import Matricula, User, Curso
from matriculas.forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'duracao_meses')  # Adicionado `duracao_meses` à lista
    search_fields = ('nome',)  # Permite pesquisar pelo nome do curso
    list_filter = ('duracao_meses',)  # Filtro lateral para duração


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'curso', 'data_matricula')
    list_filter = ('curso', 'data_matricula')  # Filtros laterais
    search_fields = ('aluno__nome', 'curso__nome')
    date_hierarchy = 'data_matricula'  # Filtro por data

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="matriculas.csv"'
        writer = csv.writer(response)
        writer.writerow(['id', 'aluno', 'curso', 'data_matricula', 'ativo']),
        for matricula in queryset:
            writer.writerow([matricula.id, matricula.aluno.nome, matricula.curso.nome,
            matricula.data_matricula, matricula.aluno.is_active,
            ])
        return response
    
    export_to_csv.short_description = 'Exportar para CSV'
    actions = [export_to_csv]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('nome', 'email', 'is_active', 'is_staff', 'is_guest')  # Adicionados campos relevantes
    search_fields = ('nome', 'email')  # Permite pesquisar por nome e email
    list_filter = ('is_active', 'is_staff', 'is_guest', 'alterou_senha')  # Filtros para status do usuário
    ordering = ('email',)  # Ordena por email
    fieldsets = (
        (None, {'fields': ('nome', 'email', 'password')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_guest', 'is_superuser','alterou_senha', 'groups', 'user_permissions')}),
        ('Datas importantes', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nome', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('last_login',)  # Exibe o último login como campo somente leitura
