from django.urls import path
from .views import CursoListView, CursoDetailView


urlpatterns = [
    path('', CursoListView.as_view(), name='lista_cursos'),
    path('<slug:slug>/', CursoDetailView.as_view(), name='curso_detail'),
]
