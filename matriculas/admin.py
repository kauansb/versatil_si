from django.contrib import admin
from matriculas.models import Matricula, User, Curso


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'curso', 'data_matricula')
    list_filter = ('curso', 'data_matricula')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('nome','email',)
    search_fields = ('nome',)

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
