from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from materiais.views import CursoListView, CursoDetailView, AlunoMateriaisView
from matriculas.views import RegisterView, LoginView, LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login' ),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('cursos/', CursoListView.as_view(), name='lista_cursos'),
    path('materiais/', AlunoMateriaisView.as_view(), name='aluno_materiais'),
    path('cursos/<int:pk>/', CursoDetailView.as_view(), name='curso_detail'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
