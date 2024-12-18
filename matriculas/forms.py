from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Curso, Matricula, Combo


class AlunoCreationForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Email")
    curso = forms.ModelMultipleChoiceField(
        queryset=Curso.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Cursos"
    )

    password1 = forms.CharField(
        required=False,  # Torna o campo de senha opcional
        widget=forms.PasswordInput,
        label="Senha (opcional)"
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
    username = forms.EmailField(label="Email")  # Usa o campo de email como username
