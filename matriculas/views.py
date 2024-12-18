from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import AlunoCreationForm, EmailAuthenticationForm


@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(permission_required('matriculas.add_matricula', raise_exception=True), name='dispatch')
class RegisterView(View):

    def get(self, request):
        # Instancia o formulário vazio
        user_form = AlunoCreationForm()
        return render(request, 'matriculas/cadastro.html', {'user_form': user_form})

    def post(self, request):
        user_form = AlunoCreationForm(request.POST)
        if user_form.is_valid():
            # Salva o formulário e cria o usuário
            user_form.save()
            messages.success(request, 'Registro realizado com sucesso! O aluno pode usar a senha padrão "senha123" para login.')
            return redirect('login')  # Redireciona para a página de login após o registro
        else:
            # Mensagens de erro detalhadas com rótulos amigáveis
            friendly_field_names = {
                'nome': 'Nome',
                'email': 'Email',
                'password1': 'Senha',
                'curso': 'Cursos'
            }
            for field, errors in user_form.errors.items():
                field_name = friendly_field_names.get(field, field)  # Rótulo amigável ou nome do campo
                for error in errors:
                    messages.error(request, f"{field_name}: {error}")
            return render(request, 'matriculas/cadastro.html', {'user_form': user_form})


class LoginView(View):

    def get(self, request):
        login_form = EmailAuthenticationForm()
        return render(request, 'matriculas/login.html', {'login_form': login_form})

    def post(self, request):
        login_form = EmailAuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = authenticate(request, username=login_form.cleaned_data['username'], password=login_form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'Login efetuado com sucesso!')
                return redirect('lista_cursos')
            else:
                messages.error(request, 'Usuário ou senha incorretos. Tente novamente.')
                login_form = EmailAuthenticationForm(data=request.POST)
        messages.error(request, 'Usuário ou senha incorretos. Tente novamente.')
        return render(request, 'matriculas/login.html', {'login_form': login_form})

class LogoutView(View):

    def get(self, request):
        logout(request)
        messages.success(request, 'Logout efetuado com sucesso!')
        return redirect('login')

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'usuario/alterar_senha.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.request.user.alterou_senha = True
        self.request.user.save()
        return response