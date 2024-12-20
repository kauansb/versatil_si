from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from .models import Curso, Material
from .forms import MaterialForm


class CursoListView(ListView):
    model = Curso
    template_name = 'materiais/lista_cursos.html'
    context_object_name = 'cursos'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('nome')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(nome__icontains=search)
            ).distinct()
        return queryset


@method_decorator(login_required(login_url='login'), name='dispatch')
class CursoDetailView(DetailView):
    model = Curso
    template_name = 'materiais/curso_detail.html'
    context_object_name = 'curso'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not request.user.is_superuser and not request.user.is_staff and obj not in request.user.cursos.all():
            messages.error(request, "Você não está matriculado neste curso.")
            return redirect('lista_cursos')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filtra os materiais apenas para o curso específico
        context['materiais'] = Material.objects.filter(curso=self.object)
        context['material_form'] = MaterialForm(initial={'curso': self.object})
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.curso = self.object
            material.save()
            messages.success(request, "Material adicionado com sucesso.")
            return redirect('curso_detail', slug=self.object.slug)
        else:
            messages.error(request, "Erro ao adicionar material.")
        return self.render_to_response(self.get_context_data(material_form=form))
