from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Escola, Professor, Aluno, Profile

class GestorRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class EscolaForm(forms.ModelForm):
    class Meta:
        model = Escola
        fields = ['nome', 'cep', 'telefone', 'tipo']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cep'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '00000-000'
        })
        self.fields['tipo'].widget.attrs.update({'class': 'form-select'})
        self.fields['tipo'].required = True
        self.fields['tipo'].label = 'Tipo de Escola'

class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['nome', 'cpf', 'email', 'telefone']

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'cpf', 'data_nascimento']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }

class ProfessorAlunosFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        # Validação adicional se necessário
        pass

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfessorEditForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['nome', 'cpf', 'email', 'telefone']

class AlunoEditForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'cpf', 'data_nascimento'] 