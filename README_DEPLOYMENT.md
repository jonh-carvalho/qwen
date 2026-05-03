# 🚀 Guia de Deploy - Django + AWS Elastic Beanstalk

## 📋 Visão Geral

Este projeto utiliza:
- **Django 6.0** com Django REST Framework
- **AWS Elastic Beanstalk** para deploy
- **RDS PostgreSQL** para banco de dados
- **GitHub Actions** para CI/CD

---

## 🔧 Pré-requisitos

1. Conta AWS configurada
2. Repositório no GitHub
3. Python 3.12+ instalado localmente
4. AWS CLI configurado (`aws configure`)

---

## 📁 Estrutura do Projeto

```
/workspace
├── .github/workflows/
│   ├── ci.yml              # Pipeline de testes
│   └── cd.yml              # Pipeline de deploy
├── .ebextensions/
│   ├── django.config       # Configurações EB
│   └── 01_django_migrations.config  # Migrations automáticas
├── aac/
│   ├── settings.py         # Configurações Django
│   ├── urls.py
│   └── wsgi.py
├── core/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── tests.py
├── .env.example            # Template de variáveis de ambiente
├── .gitignore
├── Procfile                # Configuração Gunicorn
├── requirements.txt        # Dependências Python
├── runtime.txt             # Versão do Python
└── README_DEPLOYMENT.md    # Este arquivo
```

---

## 🛠️ Configuração na AWS

### Passo 1: Criar RDS PostgreSQL

```bash
# Via AWS Console ou CLI
aws rds create-db-instance \
  --db-instance-identifier aac-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version 15 \
  --master-username postgres \
  --master-user-password SUA_SENHA_FORTE \
  --allocated-storage 20 \
  --storage-type gp2 \
  --publicly-accessible \
  --vpc-security-group-ids sg-SEU_SECURITY_GROUP \
  --db-name aac
```

**Anote as informações:**
- Endpoint: `aac-db.xxxxx.region.rds.amazonaws.com`
- Porta: `5432`
- Nome do banco: `aac`
- Usuário: `postgres`
- Senha: (sua senha)

### Passo 2: Criar Aplicação Elastic Beanstalk

```bash
# Instalar EB CLI
pip install awsebcli

# Inicializar aplicação
eb init -p python-3.12 aac-application --region us-east-1

# Criar ambiente
eb create aac-production
```

Durante a criação, informe:
- **Database type**: postgres
- **Database username**: postgres
- **Database password**: (sua senha do RDS)

### Passo 3: Configurar Variáveis de Ambiente

No console da AWS → Elastic Beanstalk → Configuration → Environment properties:

```
SECRET_KEY=sua-chave-secreta-forte-gerada-aqui
DEBUG=False
ALLOWED_HOSTS=.elasticbeanstalk.com,seu-dominio.com
DB_NAME=aac
DB_USER=postgres
DB_PASSWORD=sua-senha-rds
DB_HOST=seu-rds-endpoint.region.rds.amazonaws.com
DB_PORT=5432
```

---

## 🔐 Configurar GitHub Secrets

No GitHub do seu repositório: **Settings → Secrets and variables → Actions**

Adicione os seguintes secrets:

| Secret | Valor |
|--------|-------|
| `AWS_ACCESS_KEY_ID` | Sua AWS Access Key |
| `AWS_SECRET_ACCESS_KEY` | Sua AWS Secret Key |
| `AWS_REGION` | Região (ex: `us-east-1`) |
| `EB_APPLICATION_NAME` | Nome da aplicação EB (ex: `aac-application`) |
| `EB_ENVIRONMENT_NAME` | Nome do ambiente (ex: `aac-production`) |

---

## 🔄 Pipeline CI/CD

### CI (Continuous Integration)
Executa automaticamente em:
- Push para `main`, `master`, `develop`
- Pull Requests

**O que faz:**
1. ✅ Instala dependências
2. ✅ Roda migrations
3. ✅ Executa testes
4. ✅ Coleta static files

### CD (Continuous Deployment)
Executa automaticamente em:
- Push para `main` ou `master`

**O que faz:**
1. ✅ Configura credenciais AWS
2. ✅ Deploy automático no Elastic Beanstalk

---

## 🧪 Testes Locais

```bash
# Instalar dependências
pip install -r requirements.txt

# Criar arquivo .env
cp .env.example .env
# Edite .env com suas configurações locais

# Rodar migrações
python manage.py migrate

# Rodar testes
python manage.py test

# Rodar servidor
python manage.py runserver
```

---

## 📤 Deploy Manual (Alternativo)

```bash
# Fazer deploy manual
eb deploy

# Ver status
eb status

# Ver logs
eb logs

# Abrir aplicação
eb open
```

---

## 🔍 Monitoramento

### Logs
```bash
# Ver logs recentes
eb logs --latest

# Stream de logs em tempo real
eb logs --stream
```

### Health Check
Acesse: `http://seu-app.elasticbeanstalk.com/activities/`

### Métricas AWS
- CloudWatch: Métricas de CPU, memória, requests
- RDS: Performance do banco de dados
- Elastic Beanstalk: Health dashboard

---

## 🛡️ Segurança

### Boas Práticas Implementadas:
- ✅ `DEBUG=False` em produção
- ✅ `SECRET_KEY` via variáveis de ambiente
- ✅ `ALLOWED_HOSTS` configurado
- ✅ WhiteNoise para static files
- ✅ PostgreSQL em vez de SQLite
- ✅ Credenciais via GitHub Secrets

### Recomendações Adicionais:
1. Use HTTPS (configure SSL no Load Balancer)
2. Ative backup automático no RDS
3. Use VPC privado para o RDS
4. Configure alarmes no CloudWatch
5. Rotacione chaves de acesso periodicamente

---

## 🐛 Troubleshooting

### Erro: "Database connection failed"
- Verifique se o RDS está acessível
- Confirme security groups permitem conexão da EB
- Valide credenciais no Environment Properties

### Erro: "Static files not found"
```bash
# Rode manualmente
python manage.py collectstatic --noinput
```

### Erro: "Migrations pending"
```bash
# Rode manualmente
python manage.py migrate
```

### Ver logs detalhados
```bash
eb logs --latest
```

---

## 📚 Recursos Úteis

- [Django Deployment Checklist](https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/)
- [AWS Elastic Beanstalk Docs](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/Welcome.html)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Django REST Framework](https://www.django-rest-framework.org/)

---

## 🎯 Próximos Passos

1. [ ] Configurar domínio personalizado
2. [ ] Habilitar HTTPS/SSL
3. [ ] Configurar backups automáticos do RDS
4. [ ] Setup de ambiente de staging
5. [ ] Configurar monitoramento e alertas
6. [ ] Implementar CI/CD para múltiplos ambientes

---

**Status:** ✅ Pronto para produção!
