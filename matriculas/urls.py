from django.urls import path
from .views import RegisterView, LoginView, LogoutView, CustomPasswordChangeView, MatriculaListView, PerfilListView


urlpatterns = [
    path('', MatriculaListView.as_view(), name='lista_matriculas'),
    path('perfil/', PerfilListView.as_view(), name='perfil'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login' ),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('alterar-senha/', CustomPasswordChangeView.as_view(), name='alterar_senha'),

]
