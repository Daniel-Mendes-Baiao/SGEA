"""
Script para criar usuários de teste no SGEA.
Execute: python create_users.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sgea.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import Profile

users_data = [
    {
        'username': 'organizador@sgea.com',
        'email': 'organizador@sgea.com',
        'password': 'Admin@123',
        'role': 'organizador',
        'first_name': 'Organizador',
        'last_name': 'SGEA',
        'institution': ''
    },
    {
        'username': 'aluno@sgea.com',
        'email': 'aluno@sgea.com',
        'password': 'Aluno@123',
        'role': 'aluno',
        'first_name': 'Aluno',
        'last_name': 'SGEA',
        'institution': 'Universidade SGEA'
    },
    {
        'username': 'professor@sgea.com',
        'email': 'professor@sgea.com',
        'password': 'Professor@123',
        'role': 'professor',
        'first_name': 'Professor',
        'last_name': 'SGEA',
        'institution': 'Universidade SGEA'
    },
]

def create_users():
    print("Criando usuários de teste...")
    print("-" * 40)
    
    for data in users_data:
        user, created = User.objects.get_or_create(
            username=data['username'],
            defaults={'email': data['email']}
        )
        user.set_password(data['password'])
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.save()
        
        Profile.objects.update_or_create(
            user=user,
            defaults={
                'role': data['role'],
                'institution': data.get('institution', ''),
                'phone': '(00) 00000-0000'
            }
        )
        
        action = "✅ Criado" if created else "🔄 Atualizado"
        print(f"{action}: {data['username']} ({data['role']})")
    
    print("-" * 40)
    print("Concluído!")
    print("\nUsuários disponíveis:")
    print("  organizador@sgea.com / Admin@123")
    print("  aluno@sgea.com / Aluno@123")
    print("  professor@sgea.com / Professor@123")

if __name__ == '__main__':
    create_users()
