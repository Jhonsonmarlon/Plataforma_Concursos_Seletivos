from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (
    GestorRegistrationForm, EscolaForm, 
    ProfessorForm, AlunoForm,
    UserProfileForm, ProfileForm, ProfessorEditForm, AlunoEditForm
)
from .models import Escola, Professor, Aluno, Profile
from django.forms import modelformset_factory
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime
import io
from reportlab.lib.colors import HexColor

def home(request):
    return render(request, 'core/home.html')

def registro_gestor(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')
        
    if request.method == 'POST':
        form = GestorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Conta criada com sucesso! Agora você pode fazer login.')
            return redirect('login')
    else:
        form = GestorRegistrationForm()
    
    return render(request, 'core/registro_gestor.html', {'form': form})

@login_required
def cadastro_escola(request):
    if not request.user.is_superuser:
        return redirect('core:dashboard')
        
    if request.method == 'POST':
        form = EscolaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Escola cadastrada com sucesso!')
            return redirect('core:lista_escolas')
    else:
        form = EscolaForm()
    
    return render(request, 'core/cadastro_escola.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.is_superuser:
        # Dashboard do administrador
        context = {
            'total_escolas': Escola.objects.count(),
            'total_professores': Professor.objects.count(),
            'total_alunos': Aluno.objects.count(),
            'escolas': Escola.objects.prefetch_related(
                'professores',
                'professores__alunos'
            ).all()
        }
        return render(request, 'core/dashboard_admin.html', context)
    
    try:
        escola = request.user.escola
        context = {
            'escola': escola,
            'total_professores': escola.professores.count(),
            'total_alunos': Aluno.objects.filter(professor__escola=escola).count(),
        }
        return render(request, 'core/dashboard.html', context)
    except Escola.DoesNotExist:
        messages.warning(request, 'Cadastre sua escola primeiro.')
        return redirect('core:cadastro_escola')

@login_required
def cadastro_alunos(request, professor_id):
    professor = get_object_or_404(Professor, id=professor_id)
    
    if request.method == 'POST':
        try:
            alunos_data = []
            for key in request.POST:
                if key.startswith('alunos[') and '[nome]' in key:
                    index = key[7:key.find(']')]
                    aluno_data = {
                        'nome': request.POST.get(f'alunos[{index}][nome]'),
                        'cpf': request.POST.get(f'alunos[{index}][cpf]').replace('.', '').replace('-', ''),
                        'data_nascimento': request.POST.get(f'alunos[{index}][data_nascimento]')
                    }
                    alunos_data.append(aluno_data)
            
            # Criar alunos em lote
            for aluno_data in alunos_data:
                Aluno.objects.create(
                    professor=professor,
                    nome=aluno_data['nome'],
                    cpf=aluno_data['cpf'],
                    data_nascimento=aluno_data['data_nascimento']
                )
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return render(request, 'core/cadastro_alunos.html', {'professor': professor})

@login_required
def cadastro_professor(request):
    if not hasattr(request.user, 'escola'):
        messages.warning(request, 'Você precisa cadastrar sua escola primeiro.')
        return redirect('core:cadastro_escola')
    
    if request.method == 'POST':
        form = ProfessorForm(request.POST)
        if form.is_valid():
            professor = form.save(commit=False)
            professor.escola = request.user.escola
            professor.save()
            messages.success(request, 'Professor cadastrado com sucesso!')
            return redirect('core:inscricoes')
    else:
        form = ProfessorForm()
    
    return render(request, 'core/cadastro_professor.html', {'form': form})

@login_required
def inscricoes(request):
    escola = request.user.escola
    professores = Professor.objects.filter(escola=escola).prefetch_related('alunos')
    
    return render(request, 'core/inscricoes.html', {
        'professores': professores
    })

class GestorChangeForm(UserChangeForm):
    password = None
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

@login_required
def perfil_gestor(request):
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('core:perfil_gestor')
    else:
        user_form = UserProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    
    return render(request, 'core/perfil_gestor.html', {
        'form': user_form,
        'profile_form': profile_form
    })

@login_required
def editar_escola(request, escola_id):
    if not request.user.is_superuser:
        return redirect('core:dashboard')
        
    escola = get_object_or_404(Escola, id=escola_id)
    
    if request.method == 'POST':
        form = EscolaForm(request.POST, instance=escola)
        if form.is_valid():
            form.save()
            messages.success(request, 'Escola atualizada com sucesso!')
            return redirect('core:lista_escolas')
    else:
        form = EscolaForm(instance=escola)
    
    context = {
        'form': form,
        'escola': escola
    }
    
    return render(request, 'core/cadastro_escola.html', context)

@login_required
def perfil_admin(request):
    if not request.user.is_superuser:
        messages.error(request, 'Acesso negado.')
        return redirect('core:home')
        
    if request.method == 'POST':
        form = GestorChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('core:perfil_admin')
    else:
        form = GestorChangeForm(instance=request.user)
    
    return render(request, 'core/perfil_admin.html', {'form': form})

@login_required
def lista_professores(request):
    professores = Professor.objects.filter(escola=request.user.escola)
    return render(request, 'core/lista_professores.html', {
        'professores': professores
    })

@login_required
def lista_alunos(request, professor_id):
    professor = get_object_or_404(Professor, id=professor_id, escola=request.user.escola)
    alunos = professor.alunos.all()
    return render(request, 'core/lista_alunos.html', {
        'professor': professor,
        'alunos': alunos
    })

@login_required
def editar_professor(request, professor_id):
    professor = get_object_or_404(Professor, id=professor_id, escola=request.user.escola)
    
    if request.method == 'POST':
        form = ProfessorEditForm(request.POST, instance=professor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Professor atualizado com sucesso!')
            return redirect('core:lista_professores')
    else:
        form = ProfessorEditForm(instance=professor)
    
    return render(request, 'core/editar_professor.html', {
        'form': form,
        'professor': professor
    })

@login_required
def editar_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id, professor__escola=request.user.escola)
    
    if request.method == 'POST':
        form = AlunoEditForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aluno atualizado com sucesso!')
            return redirect('core:lista_alunos', professor_id=aluno.professor.id)
    else:
        form = AlunoEditForm(instance=aluno)
    
    return render(request, 'core/editar_aluno.html', {
        'form': form,
        'aluno': aluno
    })

@login_required
def lista_todos_alunos(request):
    alunos = Aluno.objects.filter(professor__escola=request.user.escola).select_related('professor')
    return render(request, 'core/lista_todos_alunos.html', {
        'alunos': alunos
    })

@login_required
def excluir_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id, professor__escola=request.user.escola)
    professor_id = aluno.professor.id
    
    if request.method == 'POST':
        aluno.delete()
        messages.success(request, 'Aluno excluído com sucesso!')
        
        # Verifica de onde veio a requisição
        referer = request.META.get('HTTP_REFERER', '')
        if 'lista_todos_alunos' in referer:
            return redirect('core:lista_todos_alunos')
        return redirect('core:lista_alunos', professor_id=professor_id)
    
    return redirect('core:lista_todos_alunos')

@login_required
def excluir_professor(request, professor_id):
    professor = get_object_or_404(Professor, id=professor_id, escola=request.user.escola)
    
    if request.method == 'POST':
        professor.delete()
        messages.success(request, 'Professor excluído com sucesso!')
        return redirect('core:lista_professores')
    
    return redirect('core:lista_professores')

@login_required
def dashboard_admin(request):
    if not request.user.is_superuser:
        return redirect('core:dashboard')

    tipo = request.GET.get('tipo', 'escolas')
    escola_id = request.GET.get('escola')
    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')

    # Busca todas as escolas para o filtro
    escolas = Escola.objects.all()
    
    # Inicializa as listas vazias
    escolas_lista = []
    professores = []
    alunos = []

    # Aplica os filtros baseado no tipo selecionado
    if tipo == 'escolas':
        queryset = Escola.objects.all()
        if data_inicial and data_final:
            queryset = queryset.filter(data_cadastro__range=[data_inicial, data_final])
        
        # Adiciona contagem de alunos para cada escola
        escolas_lista = queryset.annotate(
            total_alunos=Count('professores__alunos')
        )

    elif tipo == 'professores':
        queryset = Professor.objects.select_related('escola')
        if escola_id:
            queryset = queryset.filter(escola_id=escola_id)
        if data_inicial and data_final:
            queryset = queryset.filter(data_cadastro__range=[data_inicial, data_final])
        professores = queryset

    elif tipo == 'alunos':
        queryset = Aluno.objects.select_related('professor', 'professor__escola')
        if escola_id:
            queryset = queryset.filter(professor__escola_id=escola_id)
        if data_inicial and data_final:
            queryset = queryset.filter(data_cadastro__range=[data_inicial, data_final])
        alunos = queryset

    context = {
        'tipo': tipo,
        'escola_id': escola_id,
        'data_inicial': data_inicial,
        'data_final': data_final,
        'escolas': escolas,
        'escolas_lista': escolas_lista,
        'professores': professores,
        'alunos': alunos,
    }

    return render(request, 'core/dashboard_admin.html', context)

@login_required
def gerenciamento(request):
    if not request.user.is_superuser:
        return redirect('core:dashboard')

    tipo = request.GET.get('tipo')
    escola_id = request.GET.get('escola')
    professor_id = request.GET.get('professor')
    tipo_escola = request.GET.get('tipo_escola')
    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')
    pcd = request.GET.get('pcd')

    # Busca todas as escolas para o filtro
    escolas = Escola.objects.all()
    professores_lista = []
    if escola_id:
        professores_lista = Professor.objects.filter(escola_id=escola_id)
    
    # Inicializa as variáveis
    escolas_lista = []
    professores = []
    alunos = []
    resultados_filtrados = False

    if tipo:
        resultados_filtrados = True
        if tipo == 'escolas':
            queryset = Escola.objects.all()
            if tipo_escola:
                queryset = queryset.filter(is_indigena=(tipo_escola == 'indigena'))
            if data_inicial and data_final:
                queryset = queryset.filter(data_cadastro__range=[data_inicial, data_final])
            escolas_lista = queryset.annotate(total_alunos=Count('professores__alunos'))

        elif tipo == 'professores':
            queryset = Professor.objects.select_related('escola')
            if escola_id:
                queryset = queryset.filter(escola_id=escola_id)
            if data_inicial and data_final:
                queryset = queryset.filter(data_cadastro__range=[data_inicial, data_final])
            professores = queryset

        elif tipo == 'alunos':
            queryset = Aluno.objects.select_related('professor', 'professor__escola')
            if escola_id:
                queryset = queryset.filter(professor__escola_id=escola_id)
            if professor_id:
                queryset = queryset.filter(professor_id=professor_id)
            if pcd:
                queryset = queryset.filter(is_pcd=True)
            if data_inicial and data_final:
                queryset = queryset.filter(data_cadastro__range=[data_inicial, data_final])
            alunos = queryset

    context = {
        'tipo': tipo,
        'escola_id': escola_id,
        'professor_id': professor_id,
        'tipo_escola': tipo_escola,
        'data_inicial': data_inicial,
        'data_final': data_final,
        'pcd': pcd,
        'escolas': escolas,
        'professores_lista': professores_lista,
        'escolas_lista': escolas_lista,
        'professores': professores,
        'alunos': alunos,
        'resultados_filtrados': resultados_filtrados,
    }

    return render(request, 'core/gerenciamento.html', context)

@login_required
def gerar_pdf(request):
    if not request.user.is_superuser:
        return redirect('core:dashboard')

    tipo = request.GET.get('tipo')
    escola_id = request.GET.get('escola')
    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(letter),
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1
    )

    elements = []
    title = Paragraph("Sistema de Concursos e - Relatório", title_style)
    elements.append(title)

    info_style = ParagraphStyle(
        'Info',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=20
    )
    
    data_geracao = datetime.now().strftime("%d/%m/%Y %H:%M")
    filtro_info = [
        Paragraph(f"Tipo de Relatório: {tipo.title()}", info_style),
        Paragraph(f"Data de Geração: {data_geracao}", info_style),
    ]
    elements.extend(filtro_info)
    elements.append(Spacer(1, 20))

    if tipo == 'escolas':
        headers = ['Nome', 'CNPJ', 'Telefone', 'Total Professores', 'Total Alunos']
        queryset = Escola.objects.all()
        if data_inicial and data_final:
            queryset = queryset.filter(data_cadastro__range=[data_inicial, data_final])
        
        data = [[
            escola.nome,
            escola.cep,
            escola.telefone,
            str(escola.professores.count()),
            str(Aluno.objects.filter(professor__escola=escola).count())
        ] for escola in queryset]

    elif tipo == 'professores':
        headers = ['Nome', 'CPF', 'Email', 'Telefone', 'Escola', 'Total Alunos']
        queryset = Professor.objects.select_related('escola')
        if escola_id:
            queryset = queryset.filter(escola_id=escola_id)
        if data_inicial and data_final:
            queryset = queryset.filter(data_cadastro__range=[data_inicial, data_final])
        
        data = [[
            professor.nome,
            professor.cpf,
            professor.email,
            professor.telefone,
            professor.escola.nome,
            str(professor.alunos.count())
        ] for professor in queryset]

    elif tipo == 'alunos':
        headers = ['Nome', 'CPF', 'Data Nascimento', 'Professor', 'Escola']
        queryset = Aluno.objects.select_related('professor', 'professor__escola')
        if escola_id:
            queryset = queryset.filter(professor__escola_id=escola_id)
        if data_inicial and data_final:
            queryset = queryset.filter(data_cadastro__range=[data_inicial, data_final])
        
        data = [[
            aluno.nome,
            aluno.cpf,
            aluno.data_nascimento.strftime("%d/%m/%Y"),
            aluno.professor.nome,
            aluno.professor.escola.nome
        ] for aluno in queryset]

    data.insert(0, headers)
    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0275d8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
    ]))

    elements.append(table)
    doc.build(elements)
    
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Type'] = 'application/pdf'
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response

@login_required
def professores_por_escola(request, escola_id):
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Não autorizado'}, status=403)
    
    professores = Professor.objects.filter(escola_id=escola_id).values('id', 'nome')
    return JsonResponse(list(professores), safe=False)

@login_required
def lista_escolas(request):
    if not request.user.is_superuser:
        try:
            escola = Escola.objects.get(gestor=request.user)
            form = EscolaForm(instance=escola)  # Criar formulário com dados da escola
            return render(request, 'core/dados_escola.html', {
                'escola': escola,
                'form': form
            })
        except Escola.DoesNotExist:
            messages.error(request, 'Nenhuma escola associada ao seu perfil.')
            return redirect('core:dashboard')
    
    escolas = Escola.objects.all().order_by('nome')
    return render(request, 'core/lista_escolas.html', {'escolas': escolas})

@login_required
def exportar_hierarquia(request):
    if not request.user.is_superuser:
        return redirect('core:dashboard')

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(letter),
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1
    )

    elements = []
    elements.append(Paragraph("Relatório Hierárquico do Sistema", title_style))
    elements.append(Spacer(1, 20))

    escolas = Escola.objects.prefetch_related(
        'professores',
        'professores__alunos'
    ).all()

    for escola in escolas:
        # Criar dados para a tabela hierárquica
        table_data = []
        
        # Cabeçalho da escola
        table_data.append([
            Paragraph(f'<b>ESCOLA: {escola.nome.upper()}</b>'),
            Paragraph(f'<b>Tipo: {escola.get_tipo_display()}</b>'),
            Paragraph(f'<b>CEP: {escola.cep}</b>'),
            Paragraph(f'<b>Telefone: {escola.telefone}</b>')
        ])
        
        for professor in escola.professores.all():
            # Informações do professor com indentação
            table_data.append([
                Paragraph(f'    <b>PROFESSOR:</b> {professor.nome.title()}'),
                Paragraph(f'<b>Email:</b> {professor.email}'),
                Paragraph(f'<b>Telefone:</b> {professor.telefone}'),
                ''
            ])
            
            # Alunos do professor com mais indentação
            for aluno in professor.alunos.all():
                table_data.append([
                    Paragraph(f'        • {aluno.nome.title()}'),
                    '',
                    '',
                    ''
                ])
            
            # Se não houver alunos, mostrar mensagem
            if not professor.alunos.exists():
                table_data.append([
                    Paragraph('        <i>Nenhum aluno orientado</i>'),
                    '',
                    '',
                    ''
                ])
            
            # Linha em branco após cada professor
            table_data.append(['', '', '', ''])

        # Criar tabela com os dados
        table = Table(table_data, colWidths=[4*inch, 2.5*inch, 2*inch, 1.5*inch])
        
        # Estilo da tabela
        table_style = TableStyle([
            # Estilo para linha da escola
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0275d8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, 0), 1, colors.white),
            ('LINEABOVE', (0, 0), (-1, 0), 2, colors.black),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
            
            # Estilo geral
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            
            # Linhas verticais sutis
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ])
        
        # Adicionar cores alternadas para as linhas dos professores
        for i in range(len(table_data)):
            if any('PROFESSOR:' in str(cell) for cell in table_data[i]):
                table_style.add('BACKGROUND', (0, i), (-1, i), colors.HexColor('#e9ecef'))
        
        table.setStyle(table_style)
        elements.append(table)
        elements.append(Spacer(1, 20))

    # Gerar PDF
    doc.build(elements)
    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type='application/pdf')
    filename = f'Hierarquia_Sistema_{datetime.now().strftime("%Y%m%d_%H%M")}.pdf'
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response
