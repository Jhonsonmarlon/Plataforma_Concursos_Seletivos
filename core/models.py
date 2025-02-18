from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Escola(models.Model):
    TIPO_CHOICES = [
        ('estadual', 'Estadual Regular'),
        ('indigena', 'Indígena'),
    ]
    
    nome = models.CharField(max_length=200)
    cep = models.CharField(max_length=9)
    endereco = models.TextField()
    telefone = models.CharField(max_length=15)
    gestor = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Escola'
        verbose_name_plural = 'Escolas'
    
    def __str__(self):
        return self.nome

class Professor(models.Model):
    nome = models.CharField(max_length=200)
    cpf = models.CharField(
        max_length=11,
        unique=True,
        validators=[RegexValidator(r'^\d{11}$', 'CPF deve conter 11 dígitos')]
    )
    email = models.EmailField()
    telefone = models.CharField(
        max_length=11,
        validators=[RegexValidator(r'^\d{10,11}$', 'Telefone deve conter 10 ou 11 dígitos')]
    )
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE, related_name='professores')
    
    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'
    
    def __str__(self):
        return self.nome

class Aluno(models.Model):
    nome = models.CharField(max_length=200)
    cpf = models.CharField(
        max_length=11,
        unique=True,
        validators=[RegexValidator(r'^\d{11}$', 'CPF deve conter 11 dígitos')]
    )
    data_nascimento = models.DateField()
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='alunos')
    
    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'
    
    def __str__(self):
        return self.nome

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return None
