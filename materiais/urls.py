from django.urls import path
from .views import CursoListView, AlunoMateriaisView, CursoDetailView


urlpatterns = [
    path('cursos/', CursoListView.as_view(), name='lista_cursos'),
    path('materiais/', AlunoMateriaisView.as_view(), name='aluno_materiais'),
    path('cursos/<int:pk>/', CursoDetailView.as_view(), name='curso_detail'),
]
