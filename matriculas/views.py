from datetime import datetime
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from .forms import AlunoCreationForm, EmailAuthenticationForm
from .models import Matricula
from django.http import HttpResponseForbidden

@method_decorator(login_required(login_url='login'), name='dispatch')
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
            data_fim_date = datetime.strptime(data_fim, '%Y-%m-%d').date()
            queryset = [matricula for matricula in queryset if matricula.data_fim <= data_fim_date]

        return queryset
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden("Você não tem permissão para acessar esta página.")
        return super().dispatch(request, *args, **kwargs)

@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(permission_required('matriculas.add_matricula', raise_exception=True), name='dispatch')
class RegisterView(View):

    def get(self, request):
        user_form = AlunoCreationForm()
        return render(request, 'matriculas/cadastro.html', {'user_form': user_form})

    def post(self, request):
        user_form = AlunoCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Registro realizado com sucesso! O aluno pode usar a senha padrão "senha123" para login.')
            return redirect('register')  # Redireciona para a página de login após o registro
        else:
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
            user = authenticate(
                request,
                username=login_form.cleaned_data['username'],
                password=login_form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)  # Realiza o login do usuário
                messages.success(request, 'Login efetuado com sucesso!')

                # Redirecione conforme o tipo de usuário
                if user.is_superuser or user.is_staff:
                    return redirect('lista_matriculas')  # Página para admin/staff
                elif Matricula.objects.filter(aluno=user).exists():
                    return redirect('lista_cursos')  # Página para usuários matriculados
                else:
                    return redirect('home')  # Página padrão para outros casos
            else:
                messages.error(request, 'Usuário ou senha incorretos.')
        else:
            # Exibe erros específicos do formulário
            for field, errors in login_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

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