from django.shortcuts import redirect
from django.urls import reverse

class VerificaAlteracaoSenhaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Evita forçar alteração de senha para administradores ou staff
            if request.user.is_staff or request.user.is_superuser:
                return self.get_response(request)

            # Verifica se o usuário alterou a senha
            if not request.user.alterou_senha:
                # Evita redirecionar em páginas relacionadas à alteração de senha
                if not request.path.startswith(reverse('alterar_senha')):
                    return redirect('alterar_senha')

        return self.get_response(request)
