from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import AlunoCreationForm, EmailAuthenticationForm
from .models import Matricula


@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(permission_required('user.is_staff', raise_exception=True), name='dispatch')
class MatriculaListView(ListView):
    model = Matricula
    template_name = 'matriculas/lista_matriculas.html'
    context_object_name = 'matriculas'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        aluno = self.request.GET.get('aluno')
        curso = self.request.GET.get('curso')
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')

        if aluno:
            queryset = queryset.filter(aluno__nome__icontains=aluno)
        if curso:
            queryset = queryset.filter(curso__nome__icontains=curso)
        if data_inicio:
            queryset = queryset.filter(data_matricula__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data_fim__lte=data_fim)

        return queryset

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
            return redirect('register')  # Redireciona para a página de login após o registro
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