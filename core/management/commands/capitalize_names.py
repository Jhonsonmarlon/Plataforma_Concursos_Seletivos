from django.core.management.base import BaseCommand
from core.models import Escola, Professor, Aluno

class Command(BaseCommand):
    help = 'Capitaliza todos os nomes no sistema'

    def handle(self, *args, **kwargs):
        # Atualiza escolas
        for escola in Escola.objects.all():
            escola.nome = escola.nome.title()
            escola.save()
            self.stdout.write(f'Escola atualizada: {escola.nome}')
        
        # Atualiza professores
        for professor in Professor.objects.all():
            professor.nome = professor.nome.title()
            professor.save()
            self.stdout.write(f'Professor atualizado: {professor.nome}')
        
        # Atualiza alunos
        for aluno in Aluno.objects.all():
            aluno.nome = aluno.nome.title()
            aluno.save()
            self.stdout.write(f'Aluno atualizado: {aluno.nome}')
        
        self.stdout.write(self.style.SUCCESS('Todos os nomes foram capitalizados com sucesso!')) 