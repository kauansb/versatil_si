from django.contrib import admin
from matriculas.models import Matricula, User, Curso


class MatriculaAdmin(admin.ModelAdmin):
    list_display = ('aluno','curso','data_matricula',)
    search_fields = ('aluno__nome', 'curso__nome', 'data_matricula',)


class UserAdmin(admin.ModelAdmin):
    list_display = ('nome','email',)
    search_fields = ('nome',)


class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)


admin.site.register(Matricula, MatriculaAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Curso, CursoAdmin)
