# Sistema de Gestão Escolar

## Sobre o Projeto
Sistema web desenvolvido em Django para gestão de escolas, professores e alunos. Permite o cadastro e gerenciamento hierárquico de instituições de ensino, com diferentes níveis de acesso para administradores e gestores escolares.

## Funcionalidades Principais

### Administrador do Sistema
- Cadastro e gerenciamento de escolas
- Visualização de estatísticas gerais
- Geração de relatórios em PDF
- Gestão de usuários

### Gestor Escolar
- Gerenciamento de professores
- Acompanhamento de alunos
- Dashboard com informações da escola
- Edição de dados cadastrais

### Professores
- Cadastro de alunos
- Visualização de turmas
- Atualização de informações

## Tecnologias Utilizadas
- Python 3.8+
- Django 3.2+
- Bootstrap 5
- ReportLab (geração de PDFs)
- SQLite/PostgreSQL

## Instalação e Configuração

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/sistema-de-gestao-escolar.git
cd sistema-de-gestao-escolar
``` 

2. Crie e ative o ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate # Linux/Mac
``` 

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure o banco de dados:

```bash
python manage.py migrate
```

5. Crie um superusuário:

```bash
python manage.py createsuperuser
```

6. Inicie o servidor:

```bash
python manage.py runserver
```

7. Acesse a aplicação no navegador:

```bash
http://127.0.0.1:8000/
```

## Estrutura de Pastas

```bash
sistema-de-gestao-escolar/
├── core/
│   ├── __init__.py
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
├── templates/
├── static/
├── media/
├── .gitignore
├── requirements.txt
├── manage.py
├── db.sqlite3
├── .env
```


## 🔎 Funcionalidades Detalhadas

### Sistema de Usuários
- Superadmin: Acesso total ao sistema
- Gestor: Gerenciamento da própria escola
- Autenticação e autorização personalizada

### Dashboard Administrativo
- Total de escolas no sistema
- Total de professores
- Total de alunos
- Lista de escolas recentes
- Geração de relatórios em PDF

### Dashboard do Gestor
- Total de professores da escola
- Total de alunos da escola
- Ações rápidas para cadastros
- Sistema de inscrições

### Gestão de Professores
- Cadastro de professores
- Vinculação automática com escola
- Listagem de alunos por professor
- Edição e gerenciamento

### Gestão de Alunos
- Cadastro de alunos
- Vinculação com professores
- Listagem completa
- Sistema de busca e filtros

## 🛠️ Comandos Úteis


## 👥 Níveis de Acesso

1. **Administrador (Superuser)**
   - Acesso total ao sistema
   - Gerenciamento de escolas
   - Visualização de todos os dados
   - Geração de relatórios

2. **Gestor Escolar**
   - Gerenciamento da própria escola
   - Controle de professores
   - Gestão de alunos
   - Acesso ao dashboard escolar

## 📝 Funcionalidades Específicas

### Relatórios
- Geração de PDF com hierarquia completa
- Listagem de escolas, professores e alunos
- Formatação profissional
- Cabeçalho e rodapé personalizados

### Sistema de Inscrições
- Cadastro de alunos por professor
- Validação de dados
- Interface intuitiva
- Confirmação automática

## 🔒 Segurança

- Autenticação obrigatória
- Proteção contra CSRF
- Validação de formulários
- Permissões baseadas em usuário

## 📊 Modelos de Dados

### Escola
- Nome
- Tipo (Pública/Privada)
- Gestor (User)
- Data de cadastro

### Professor
- Nome
- Email
- Telefone
- Escola (ForeignKey)

### Aluno
- Nome
- CPF
- Data de nascimento
- Professor (ForeignKey)

## 📄 Notas de Versão

* 1.0.0
    * Sistema base implementado
    * Dashboard administrativo e escolar
    * Sistema de inscrições
    * Geração de relatórios
    * Capitalização automática de nomes

## ✒️ Autor

* **Jhonson** - *Desenvolvimento*

## 📌 Observações

- Sistema em desenvolvimento ativo
- Backup automático do banco de dados recomendado
- Manter ambiente virtual atualizado
- Verificar atualizações de segurança

---
⌨️ com ❤️ por [Jhonson](https://github.com/Jhonsonmarlon)









