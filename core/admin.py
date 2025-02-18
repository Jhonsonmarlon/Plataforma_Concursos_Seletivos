from django.contrib import admin
from .models import Escola, Professor, Aluno

@admin.register(Escola)
class EscolaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cep', 'telefone', 'tipo', 'gestor']
    search_fields = ['nome', 'cep']
    list_filter = ['tipo']

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'telefone', 'escola']
    search_fields = ['nome', 'email']
    list_filter = ['escola']

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf', 'data_nascimento', 'professor']
    search_fields = ['nome', 'cpf']
    list_filter = ['professor']
