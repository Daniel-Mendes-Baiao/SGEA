from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import re
from .models import Profile

# Formulário de cadastro simples (estilo aluno): cria User + Profile com validações básicas.
class SignUpForm(forms.Form):
    username = forms.CharField(label='Usuário', max_length=150)
    first_name = forms.CharField(label='Nome', max_length=150, required=False)
    last_name = forms.CharField(label='Sobrenome', max_length=150, required=False)
    email = forms.EmailField(label='E-mail', required=False)
    phone = forms.CharField(label='Telefone', max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'phone-mask', 'placeholder': '(00) 00000-0000'}))
    institution = forms.CharField(label='Instituição (obrigatório p/ aluno/prof.)', max_length=200, required=False)
    role = forms.ChoiceField(label='Perfil', choices=Profile.ROLE_CHOICES)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput, 
                               help_text='Mínimo 8 caracteres, contendo letras, números e caracteres especiais.')
    password2 = forms.CharField(label='Confirmar senha', widget=forms.PasswordInput)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        if len(password) < 8:
            raise forms.ValidationError('A senha deve ter no mínimo 8 caracteres.')
        
        if not re.search(r'[A-Za-z]', password):
            raise forms.ValidationError('A senha deve conter pelo menos uma letra.')
        
        if not re.search(r'\d', password):
            raise forms.ValidationError('A senha deve conter pelo menos um número.')
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise forms.ValidationError('A senha deve conter pelo menos um caractere especial (!@#$%^&*(),.?":{}|<>).')
        
        return password

    def clean(self):
        data = super().clean()
        if data.get('password') != data.get('password2'):
            self.add_error('password2','Senhas não conferem.')
        role = data.get('role')
        inst = data.get('institution','').strip()
        if role in ('aluno','professor') and not inst:
            self.add_error('institution','Instituição é obrigatória para aluno/professor.')
        return data

    def save(self):
        u = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data.get('first_name',''),
            last_name=self.cleaned_data.get('last_name',''),
            email=self.cleaned_data.get('email',''),
        )
        Profile.objects.create(
            user=u,
            phone=self.cleaned_data.get('phone',''),
            institution=self.cleaned_data.get('institution',''),
            role=self.cleaned_data['role'],
        )
        return u
