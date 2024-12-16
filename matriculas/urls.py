from django.urls import path
from .views import RegisterView, LoginView, LogoutView, CustomPasswordChangeView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login' ),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('alterar-senha/', CustomPasswordChangeView.as_view(), name='alterar_senha'),

    #path('alterar-senha/', PasswordChangeView.as_view(
    #    template_name='usuario/alterar_senha.html',
    #    success_url='/alterar-senha-concluida/'
    #), name='alterar_senha'),
    #
    #path('alterar-senha-concluida/', PasswordChangeDoneView.as_view(
    #    template_name='usuario/alterar_senha_concluida.html'
    #), name='alterar_senha_concluida'),
]
