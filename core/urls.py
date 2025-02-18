from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('registro/', views.registro_gestor, name='registro_gestor'),
    path('escola/cadastro/', views.cadastro_escola, name='cadastro_escola'),
    path('professor/cadastro/', views.cadastro_professor, name='cadastro_professor'),
    path('professor/<int:professor_id>/alunos/', views.cadastro_alunos, name='cadastro_alunos'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('inscricoes/', views.inscricoes, name='inscricoes'),
    path('logout/', LogoutView.as_view(next_page='core:home'), name='logout'),
    path('perfil/', views.perfil_gestor, name='perfil_gestor'),
    path('perfil/admin/', views.perfil_admin, name='perfil_admin'),
    path('escola/editar/<int:escola_id>/', views.editar_escola, name='editar_escola'),
    path('escola/editar/', views.lista_escolas, name='redirecionar_lista'),
    path('professor/<int:professor_id>/editar/', views.editar_professor, name='editar_professor'),
    path('aluno/<int:aluno_id>/editar/', views.editar_aluno, name='editar_aluno'),
    path('professores/', views.lista_professores, name='lista_professores'),
    path('professor/<int:professor_id>/alunos/', views.lista_alunos, name='lista_alunos'),
    path('alunos/', views.lista_todos_alunos, name='lista_todos_alunos'),
    path('aluno/<int:aluno_id>/excluir/', views.excluir_aluno, name='excluir_aluno'),
    path('professor/<int:professor_id>/excluir/', views.excluir_professor, name='excluir_professor'),
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    path('gerenciamento/', views.gerenciamento, name='gerenciamento'),
    path('gerenciamento/pdf/', views.gerar_pdf, name='gerar_pdf'),
    path('gerenciamento/hierarquia/pdf/', views.exportar_hierarquia, name='exportar_hierarquia'),
    path('api/professores-por-escola/<int:escola_id>/', views.professores_por_escola, name='professores_por_escola'),
    path('escolas/', views.lista_escolas, name='lista_escolas'),
] 