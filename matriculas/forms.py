from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Curso, Matricula


class AlunoCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    curso = forms.ModelMultipleChoiceField(queryset=Curso.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = User
        fields = ("nome", "email", "password1", "password2", "curso")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email já está em uso.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            cursos = self.cleaned_data["curso"]
            for curso in cursos:
                Matricula.objects.create(aluno=user, curso=curso)
        return user


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")  # Usa o campo de email como username
