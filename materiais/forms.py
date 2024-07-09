from django import forms
from matriculas.models import Curso
from .models import Material


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nome', 'imagem']

    def clean_imagem(self):
        imagem = self.cleaned_data.get('imagem')
        if imagem:
            if not imagem.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                raise forms.ValidationError('Somente arquivos PNG, JPG, JPEG e GIF são suportados.')
        return imagem


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['nome', 'descricao', 'arquivo', 'curso']
        widgets = {
            'curso': forms.HiddenInput(),
            'descricao': forms.Textarea(attrs={'cols': 50, 'rows': 3}),  # Define o tamanho do textarea
        }
