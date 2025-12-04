# 🧩 SGEA — Sistema de Gestão de Eventos Acadêmicos

Sistema desenvolvido em **Django** para gerenciamento completo de eventos acadêmicos com:
- ✅ Cadastro e inscrição em eventos com validação avançada
- ✅ Emissão automática de certificados (PDF)
- ✅ Geração de relatórios (CSV e PDF)
- ✅ Controle de perfis (Aluno, Professor, Organizador)
- ✅ API REST com autenticação por token e rate limiting
- ✅ Upload e validação de banners de eventos

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
git clone https://github.com/seuusuario/SGEA.git
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

Execute o script para popular o banco com usuários padrão:

```bash
python create_users.py
```

**Usuários criados:**
- `organizador@sgea.com` / `Admin@123` (Organizador)
- `aluno@sgea.com` / `Aluno@123` (Aluno)
- `professor@sgea.com` / `Professor@123` (Professor)

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
   - **Banner**: Tente enviar arquivo .txt (deve dar erro)
4. Salve e verifique se o banner aparece na página de detalhes

#### 3. Teste de Inscrição (Aluno/Professor)
1. Faça login como `aluno@sgea.com`
2. Acesse a lista de eventos
3. Clique em um evento e inscreva-se
4. Tente se inscrever novamente (deve mostrar mensagem de duplicidade)
5. Crie um evento com capacidade 1 (como organizador)
6. Inscreva 2 usuários diferentes (o segundo deve receber erro de capacidade esgotada)

#### 4. Teste de Relatórios (Organizador)
1. Faça login como `organizador@sgea.com`
2. Acesse a lista de eventos
3. Clique em "Relatório" de um evento com inscrições
4. Baixe CSV e PDF
5. Verifique se os dados estão corretos

#### 5. Teste de API REST

**5.1. Obter Token:**
```bash
curl -X POST http://localhost:8000/api/token/ \
  -d "username=aluno@sgea.com&password=Aluno@123"
```

**5.2. Listar Eventos:**
```bash
curl -X GET http://localhost:8000/api/events/ \
  -H "Authorization: Token SEU_TOKEN_AQUI"
```

**5.3. Inscrever em Evento:**
```bash
curl -X POST http://localhost:8000/api/enroll/1/ \
  -H "Authorization: Token SEU_TOKEN_AQUI"
```

**5.4. Teste de Rate Limiting:**
- Execute o script de teste: `python test_api.py`
- Faça mais de 20 requisições para `/api/events/` no mesmo dia
- Verifique se recebe erro 429 (Too Many Requests)

**5.5. Teste de Autenticação:**
```bash
curl -X GET http://localhost:8000/api/events/
```
Deve retornar erro 401 (Unauthorized)

---

## 🚀 Funcionalidades

### Validação Avançada de Formulários
- **Máscara de Telefone**: `(XX) XXXXX-XXXX` com jQuery Mask Plugin
- **Datepicker**: jQuery UI para seleção de datas
- **Validação de Email**: Campo `EmailField` com validação automática
- **Validação de Capacidade**: Apenas números positivos
- **Validação de Banner**: Apenas arquivos de imagem (MIME type check)

### Controle de Perfis
| Perfil | Permissões |
|--------|-----------|
| **Organizador** | Criar eventos, gerar relatórios, emitir certificados |
| **Aluno** | Inscrever-se em eventos, visualizar certificados |
| **Professor** | Inscrever-se em eventos, visualizar certificados |

### Páginas Principais
| Função | URL | Acesso |
|--------|-----|--------|
| Página inicial | `/` | Público |
| Listar eventos | `/events/` | Público |
| Criar evento | `/events/novo/` | Organizador |
| Detalhes do evento | `/events/<id>/` | Público |
| Relatório de inscritos | `/reports/event/<id>/` | Organizador |
| Exportar CSV | `/reports/event/<id>/csv/` | Organizador |
| Exportar PDF | `/reports/event/<id>/pdf/` | Organizador |

---

## 🔌 API REST

### Autenticação
Todas as requisições exigem token de autenticação:

```bash
Authorization: Token SEU_TOKEN_AQUI
```

### Endpoints

#### 1. Obter Token
```http
POST /api/token/
Content-Type: application/x-www-form-urlencoded

username=aluno@sgea.com&password=Aluno@123
```

**Response:**
```json
{
  "token": "eb231fdba3346e439a61bb66fac835462806dd0d"
}
```

#### 2. Listar Eventos
```http
GET /api/events/
Authorization: Token {token}
```

**Rate Limit:** 20 requisições/dia

**Response:**
```json
[
  {
    "id": 1,
    "title": "Workshop de Django",
    "event_type": "workshop",
    "start_date": "2025-12-01",
    "end_date": "2025-12-01",
    "place": "Sala 101",
    "organizer": "organizador@sgea.com"
  }
]
```

#### 3. Inscrever em Evento
```http
POST /api/enroll/{event_id}/
Authorization: Token {token}
```

**Rate Limit:** 50 requisições/dia

**Response:**
```json
{
  "message": "Successfully enrolled in event."
}
```

### Rate Limiting
| Endpoint | Limite |
|----------|--------|
| `/api/events/` | 20 req/dia |
| `/api/enroll/<id>/` | 50 req/dia |

---

## 📁 Estrutura do Projeto

```
SGEA/
├── accounts/           # Gestão de usuários e perfis
├── api/                # API REST com DRF
├── certificates/       # Emissão de certificados
├── core/               # Configurações básicas
├── events/             # CRUD de eventos
├── registrations/      # Inscrições
├── reports/            # Relatórios e exportações
├── sgea/               # Configuração Django
├── templates/          # Templates HTML
├── media/              # Uploads (banners)
├── static/             # CSS, JS
├── create_users.py     # Script para criar usuários
├── test_api.py         # Script de teste da API
├── manage.py
└── requirements.txt
```

---

## 👨‍💻 Autores

Desenvolvido por **Daniel Mendes** e **Luiz Filipe**  
Projeto acadêmico - Sistema de Gestão de Eventos Acadêmicos (SGEA)

---

## 📄 Licença

Este projeto é de uso acadêmico.