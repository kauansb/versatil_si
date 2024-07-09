from django.db import models
from matriculas.models import Curso


class Material(models.Model):
    curso = models.ForeignKey(Curso, related_name='materiais', on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    arquivo = models.FileField(upload_to='materiais/')

    def __str__(self):
        return self.nome
