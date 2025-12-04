# 🧩 SGEA — Sistema de Gestão de Eventos Acadêmicos

![SGEA Logo](static/logo.jpg)

Sistema desenvolvido em **Django** para gerenciamento completo de eventos acadêmicos com:
- ✅ Cadastro e inscrição em eventos com validação avançada
- ✅ Emissão automática de certificados (PDF)
- ✅ Geração de relatórios (CSV e PDF)
- ✅ Controle de perfis (Aluno, Professor, Organizador)
- ✅ API REST com autenticação por token e rate limiting
- ✅ Upload e validação de banners de eventos
- ✅ Sistema de auditoria completo
- ✅ Identidade visual moderna e acessível

---

## 📋 Índice

- [Requisitos](#-requisitos)
- [Guia de Instalação](#️-guia-de-instalação)
- [Guia de Testes](#-guia-de-testes)
- [Funcionalidades](#-funcionalidades)
- [API REST](#-api-rest)
- [Estrutura do Projeto](#-estrutura-do-projeto)

---

## 🔧 Requisitos

- **Python 3.12+** → [Download](https://www.python.org/downloads/)
- **pip** (gerenciador de pacotes Python)
- **Git** (opcional, para clonar o repositório)

---

## ⚙️ Guia de Instalação

### 1️⃣ Clonar o Repositório

```bash
git clone https://github.com/Daniel-Mendes-Baiao/SGEA.git
cd SGEA
```

Ou baixe o `.zip` e extraia em uma pasta local.

### 2️⃣ Criar Ambiente Virtual

```bash
python -m venv venv
```

**Ativar no Windows (PowerShell):**
```powershell
venv\Scripts\activate
```

**Ativar no Linux/Mac:**
```bash
source venv/bin/activate
```

> ⚠️ **Erro de permissão no Windows?**  
> Execute: `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`

### 3️⃣ Instalar Dependências

```bash
pip install -r requirements.txt
```

**Dependências incluídas:**
- Django 5.x
- djangorestframework
- reportlab (geração de PDFs)
- Pillow (processamento de imagens)

### 4️⃣ Configurar Banco de Dados

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Criar Usuários de Teste

Execute o script para criar usuários padrão:

```bash
python create_users.py
```

**Usuários criados:**
| Usuário | Senha | Perfil |
|---------|-------|--------|
| `organizador@sgea.com` | `Admin@123` | Organizador |
| `aluno@sgea.com` | `Aluno@123` | Aluno |
| `professor@sgea.com` | `Professor@123` | Professor |

### 6️⃣ Rodar o Servidor

```bash
python manage.py runserver
```

Acesse: **http://localhost:8000**

---

## 🧪 Guia de Testes

### Roteiro de Testes Funcionais

#### 1. Teste de Cadastro e Login
1. Acesse `/accounts/signup/`
2. Preencha o formulário com:
   - **Telefone**: Digite números e verifique a máscara `(XX) XXXXX-XXXX`
   - **Email**: Teste com email inválido (ex: `teste@`)
   - **Perfil**: Selecione "Aluno" ou "Professor"
   - **Instituição**: Deixe em branco e verifique erro de validação
3. Faça login com as credenciais criadas

#### 2. Teste de Criação de Evento (Organizador)
1. Faça login como `organizador@sgea.com`
2. Acesse `/events/novo/`
3. Preencha o formulário:
   - **Data Inicial/Final**: Clique e verifique o datepicker
   - **Horário**: Digite e verifique a máscara `00:00`
   - **Capacidade**: Tente valor negativo (deve dar erro)
   - **Banner**: Faça upload de uma imagem (PNG/JPG)
4. Salve e verifique se o banner aparece na página de detalhes

#### 3. Teste de Inscrição (Aluno/Professor)
1. Faça login como `aluno@sgea.com`
2. Acesse a lista de eventos
3. Clique em um evento e inscreva-se
4. Tente se inscrever novamente (deve mostrar mensagem de duplicidade)

#### 4. Teste de Cancelamento de Inscrição
1. Faça login como aluno inscrito em um evento
2. Acesse os detalhes do evento
3. Clique em "Cancelar Inscrição"
4. Confirme o cancelamento

#### 5. Teste de Auditoria (Organizador)
1. Faça login como organizador
2. Acesse `/audit/`
3. Verifique os logs de ações do sistema
4. Teste os filtros por data e usuário

#### 6. Teste de API REST

**Obter Token:**
```bash
curl -X POST http://localhost:8000/api/auth/ \
  -d "username=aluno@sgea.com&password=Aluno@123"
```

**Listar Eventos:**
```bash
curl -X GET http://localhost:8000/api/events/ \
  -H "Authorization: Token SEU_TOKEN_AQUI"
```

---

## 🚀 Funcionalidades

### Controle de Perfis
| Perfil | Permissões |
|--------|-----------|
| **Organizador** | Criar eventos, gerar relatórios, emitir certificados, ver auditoria, cadastrar usuários |
| **Aluno** | Inscrever-se em eventos, cancelar inscrição, visualizar certificados |
| **Professor** | Inscrever-se em eventos, cancelar inscrição, visualizar certificados |

### Sistema de Auditoria
O sistema registra automaticamente:
- Criação, alteração e exclusão de eventos
- Inscrições e cancelamentos
- Criação de usuários por organizadores
- Geração e download de certificados
- Consultas via API

### Páginas Principais
| Função | URL | Acesso |
|--------|-----|--------|
| Página inicial | `/` | Público |
| Listar eventos | `/events/` | Público |
| Criar evento | `/events/novo/` | Organizador |
| Logs de auditoria | `/audit/` | Organizador |
| Meus certificados | `/certificates/my/` | Aluno/Professor |

---

## 🔌 API REST

### Endpoints

| Endpoint | Método | Descrição | Rate Limit |
|----------|--------|-----------|------------|
| `/api/auth/` | POST | Obter token | - |
| `/api/events/` | GET | Listar eventos | 20/dia |
| `/api/enroll/` | POST | Inscrever em evento | 50/dia |

---

## 📁 Estrutura do Projeto

```
SGEA/
├── accounts/           # Gestão de usuários e perfis
├── api/                # API REST com DRF
├── audit/              # Sistema de auditoria
├── certificates/       # Emissão de certificados
├── core/               # Configurações básicas
├── docs/               # Documentação
├── events/             # CRUD de eventos
├── registrations/      # Inscrições e cancelamentos
├── reports/            # Relatórios e exportações
├── sgea/               # Configuração Django
├── static/             # CSS, JS, Logo
├── templates/          # Templates HTML
├── create_users.py     # Script para criar usuários de teste
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🎨 Identidade Visual

O sistema utiliza uma paleta de cores baseada em azul marinho (#1e3a5f) com:
- Design responsivo (mobile-first)
- Acessibilidade (ARIA labels, skip links)
- Bootstrap 5 + Bootstrap Icons

---

## 👨‍💻 Autores

Desenvolvido por **Daniel Mendes** e **Luiz Filipe**  
Projeto acadêmico - Sistema de Gestão de Eventos Acadêmicos (SGEA)

---

## 📄 Licença

Este projeto é de uso acadêmico.
