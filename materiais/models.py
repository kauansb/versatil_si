from django.db import models
from matriculas.models import Curso


class Material(models.Model):
    TIPO_MATERIAL_CHOICES = [
        ('apostila', 'Apostila'),
        ('exercicio', 'Exercício'),
        ('outro', 'Outro'),
    ]

    curso = models.ForeignKey(Curso, related_name='materiais', on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=TIPO_MATERIAL_CHOICES, default='outro')
    arquivo = models.FileField(upload_to='materiais/')
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Renomeia o arquivo baseado no nome do material
        if not self.pk:  # Somente no momento da criação
            self.arquivo.name = f'{self.nome}-{self.arquivo.name}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome
