from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import User, Curso, Matricula


class AlunoCreationForm(forms.ModelForm):
    nome = forms.CharField(
        required=True,
        label='Nome', 
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(
        required=True, 
        label="Email", 
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    curso = forms.ModelMultipleChoiceField(
        required=True,
        queryset=Curso.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Cursos"
    )

    password1 = forms.CharField(
        required=False,  # Torna o campo de senha opcional
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Senha (opcional)",
        strip=False,
    )

    class Meta:
        model = User
        fields = ("nome", "email", "curso", "password1")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email já está em uso.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        # Define uma senha padrão se o campo password1 estiver vazio
        senha = self.cleaned_data.get("password1")
        if senha:
            user.set_password(senha)
        else:
            user.set_password("senha123")  # Senha padrão

        if commit:
            user.save()

            # Matrícula nos cursos individuais
            cursos = self.cleaned_data.get("curso")
            for curso in cursos:
                Matricula.objects.create(aluno=user, curso=curso)
        return user


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Senha",
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError("Esta conta está inativa.", code="inactive")

        if user.is_staff or user.is_superuser:
            return
        
        if Matricula.objects.filter(aluno=user).exists():
            return
        
        if getattr(user, "is_guest", False):
            return
        
        raise forms.ValidationError("Você não está matriculado em nenhum curso ou autorizado a acessar.", code="no_matricula")

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'nome')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Garante que a senha seja encriptada
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'nome', 'is_active', 'is_staff')