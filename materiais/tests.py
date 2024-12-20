from django.test import TestCase
from django.urls import reverse
from .models import Curso

class CursoModelTest(TestCase):

    def setUp(self):
        self.curso = Curso.objects.create(
            nome='Curso de Teste',
            imagem=None,
            slug='curso-de-teste',
            duracao_meses=6
        )

    def test_curso_creation(self):
        self.assertEqual(self.curso.nome, 'Curso de Teste')
        self.assertEqual(self.curso.slug, 'curso-de-teste')
        self.assertEqual(self.curso.duracao_meses, 6)

    def test_curso_str(self):
        self.assertEqual(str(self.curso), 'Curso de Teste')

    def test_slug_generation(self):
        curso = Curso.objects.create(nome='Novo Curso')
        self.assertEqual(curso.slug, 'novo-curso')


class CursoListViewTest(TestCase):

    def setUp(self):
        self.curso1 = Curso.objects.create(nome='Curso 1', slug='curso-1', duracao_meses=6)
        self.curso2 = Curso.objects.create(nome='Curso 2', slug='curso-2', duracao_meses=6)

    def test_curso_list_view_status_code(self):
        response = self.client.get(reverse('lista_cursos'))
        self.assertEqual(response.status_code, 200)

    def test_curso_list_view_template(self):
        response = self.client.get(reverse('lista_cursos'))
        self.assertTemplateUsed(response, 'materiais/lista_cursos.html')

    def test_curso_list_view_context(self):
        response = self.client.get(reverse('lista_cursos'))
        self.assertIn('cursos', response.context)
        self.assertEqual(len(response.context['cursos']), 2)

    def test_curso_list_view_search(self):
        response = self.client.get(reverse('lista_cursos'), {'search': 'Curso 1'})
        self.assertEqual(len(response.context['cursos']), 1)
        self.assertEqual(response.context['cursos'][0].nome, 'Curso 1')