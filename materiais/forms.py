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
    nome = forms.CharField(label='Nome',
                           max_length=255,
                           widget=forms.TextInput(attrs={'class': 'form-control'}),
                           required=True)
    descricao = forms.CharField(label='Descrição',
                                widget=forms.Textarea(attrs={'class': 'form-control'}),
                                required=False)
    tipo = forms.ChoiceField(label='Tipo',
                             choices=Material.TIPO_MATERIAL_CHOICES,
                             widget=forms.Select(attrs={'class': 'form-control'}))
    arquivo = forms.FileField(label='Arquivo',
                              widget=forms.FileInput(attrs={'class': 'form-control'}),
                              required=True)

    class Meta:
        model = Material
        fields = ['nome', 'descricao', 'tipo', 'arquivo']
        widgets = {
            'descricao': forms.Textarea(attrs={'cols': 50, 'rows': 3}),
            'tipo': forms.Select(),
        }

    def clean_arquivo(self):
        arquivo = self.cleaned_data.get('arquivo')
        if arquivo:
            # Restrição para arquivos de tamanho até 10 MB
            if arquivo.size > 10 * 1024 * 1024:
                raise forms.ValidationError('O arquivo deve ter no máximo 10MB.')
        return arquivo
