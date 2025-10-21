# 🛡️ Sprint 4 - Aplicação Flask Segura com Análise de Vulnerabilidades

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![Security](https://img.shields.io/badge/Security-Analysis-red.svg)](https://github.com/9luis7/sprint4-secure-ml-app)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Projeto educacional de segurança cibernética** demonstrando vulnerabilidades comuns em aplicações web e suas respectivas mitigações.

## 📋 Índice
- [🎯 O Desafio (A Aplicação Vulnerável)](#-o-desafio-a-aplicação-vulnerável)
- [🚨 Prova do Crime (Ataques Executados)](#-prova-do-crime-ataques-executados)
- [🛡️ A Blindagem (Proteções Implementadas)](#️-a-blindagem-proteções-implementadas)
- [🧪 Validação (O "Antes e Depois")](#-validação-o-antes-e-depois)
- [📊 Arquitetura e Resiliência (Defesa em Profundidade)](#-arquitetura-e-resiliência-defesa-em-profundidade)
- [👥 Equipe](#-equipe)
- [🚀 Como Executar](#-como-executar)
- [📚 Recursos](#-recursos)

## 🎯 O Desafio (A Aplicação Vulnerável)

### 👥 Equipe
| Nome | RM | Função |
|------|----|---------| 
| **Luis Fernando de Oliveira Salgado** | 561401 | Desenvolvimento & Segurança |
| **Bernardo Braga Perobeli** | 562468 | Análise de Vulnerabilidades |
| **Lucca Phelipe Masini** | 564121 | Documentação & Testes |
| **Igor Paixão Sarak** | 563726 | Arquitetura & Mitigações |

### 🎯 O Cenário
Este projeto nasceu de um **desafio educacional**: criar uma aplicação Flask de machine learning que **intencionalmente** possuísse vulnerabilidades de segurança para fins de estudo. O objetivo era demonstrar diferentes tipos de ataques cibernéticos e suas respectivas mitigações, implementando uma arquitetura de **defesa em profundidade**.

### 📁 Estrutura do Projeto
```
sprint4-secure-ml-app/
├── sprint4_app/
│   ├── app.py                          # 🚀 Aplicação Flask principal
│   ├── create_model.py                 # 🧠 Script para criar modelo ML
│   ├── internal_service.py             # 🔒 Serviço interno simulado
│   ├── security_attack_flowcharts.md   # 📊 Diagramas de segurança
│   ├── requirements.txt                # 📦 Dependências Python
│   └── model.pkl                       # 🤖 Modelo de ML treinado
└── README.md                           # 📖 Documentação principal
```

### 🛡️ Arquitetura de Segurança

```mermaid
graph TD
    User["👤 Usuário / Atacante"] --> WAF["🛡️ WAF / Firewall"];
    
    subgraph "Infraestrutura do Servidor Protegida"
        WAF --> AppServer["🖥️ Servidor da Aplicação"];
        subgraph AppServer
            RateLimiter["⏱️ Rate Limiter (Anti-DoS)"];
            URLValidator["✅ Validador de URL (Anti-SSRF)"];
            MLModel["🧠 Modelo de ML"];
        end
        AppServer --> RateLimiter --> URLValidator --> MLModel;
    end

    subgraph "Resiliência"
        BackupService["☁️ Serviço de Backup Externo"];
    end

    AppServer -.->|"Backups Regulares"| BackupService;

    style User fill:#2ecc71,stroke:#27ae60,stroke-width:2px,color:#fff
    style WAF fill:#3498db,stroke:#2980b9,stroke-width:2px,color:#fff
    style AppServer fill:#95a5a6,stroke:#7f8c8d,stroke-width:2px,color:#fff
    style RateLimiter fill:#e67e22,stroke:#d35400,stroke-width:2px,color:#fff
    style URLValidator fill:#e74c3c,stroke:#c0392b,stroke-width:2px,color:#fff
    style MLModel fill:#9b59b6,stroke:#8e44ad,stroke-width:2px,color:#fff
    style BackupService fill:#34495e,stroke:#2c3e50,stroke-width:2px,color:#fff
```

## 🚨 Prova do Crime (Ataques Executados)

O projeto começou identificando as **três falhas principais** que tornavam a aplicação vulnerável. Cada uma representava um vetor de ataque diferente, demonstrando como vulnerabilidades aparentemente simples podem ser exploradas de forma devastadora.

### 1. 🕵️ SSRF (Server-Side Request Forgery) - **VULNERABILIDADE PURA**
- **Endpoint afetado**: `/predict`
- **Parâmetro vulnerável**: `image_url`
- **Vulnerabilidade**: Aplicação fazia requisições HTTP para qualquer URL fornecida
- **Risco**: Acesso a recursos internos do servidor
- **Payload de ataque**: `http://localhost:5000/predict?image_url=http://127.0.0.1:8080/admin`
- **Consequência**: Atacante podia acessar painel admin interno

### 2. 💥 DoS (Denial of Service) - **VULNERABILIDADE PURA**
- **Causa**: Ausência de rate limiting + carga de trabalho pesada
- **Simulação**: `time.sleep(0.5)` em cada requisição
- **Risco**: Sobrecarga do servidor com requisições simultâneas
- **Impacto**: Indisponibilidade total do serviço
- **Consequência**: Usuários legítimos bloqueados

### 3. 🔒 Ransomware - **VULNERABILIDADE PURA**
- **Vetor**: Exploração das vulnerabilidades anteriores
- **Alvo**: Arquivos críticos (`app.py`, `model.pkl`)
- **Consequência**: Criptografia e inutilização dos arquivos
- **Risco**: Perda total de dados e aplicação

## 🛡️ A Blindagem (Proteções Implementadas)

Após o sucesso dos ataques, implementamos as correções para fechar as brechas. Cada vulnerabilidade recebeu sua respectiva mitigação, transformando a aplicação em um sistema robusto e seguro.

### ✅ **Rate Limiting (Anti-DoS)**
```python
# Flask-Limiter com 10 requisições por minuto por IP
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10 per minute"],
    storage_uri="memory://"
)
```

### ✅ **Validação de URL (Anti-SSRF)**
```python
# Whitelist de domínios permitidos
ALLOWED_DOMAINS = {'i.imgur.com', 'images.pexels.com'}

# Validação de esquema e domínio
if parsed_url.scheme not in ['http', 'https']:
    return jsonify({'error': 'URL inválida ou não permitida.'}), 403
```

### ✅ **Simulação de Carga**
```python
# Simulação de processamento pesado
time.sleep(0.5)  # 500ms de delay por requisição
```

## 🚀 Como Executar

### 📋 Pré-requisitos
- **Python 3.7+**
- **pip** (gerenciador de pacotes Python)
- **Git** (para clonar o repositório)

### 🔧 Instalação
```bash
# 1. Clonar o repositório
git clone https://github.com/9luis7/sprint4-secure-ml-app.git
cd sprint4-secure-ml-app/sprint4_app

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Executar a aplicação
python app.py
```

### 🧪 Demonstração de Segurança
```bash
# Terminal 1: Aplicação principal (porta 5000)
cd sprint4_app
python app.py

# Terminal 2: Serviço interno (porta 8080)
python internal_service.py
```

### 🌐 Endpoints
| Serviço | URL | Descrição |
|---------|-----|-----------|
| **Aplicação Principal** | http://localhost:5000 | API Flask protegida |
| **Serviço Interno** | http://localhost:8080 | Simulação de recurso interno |
| **Endpoint API** | `/predict?image_url=<URL>` | Predição de ML com validações |
| **Admin Interno** | `/admin` | Endpoint que deveria ser privado |

## 🧪 Validação (O "Antes e Depois")

Esta seção serve para **provar que as mitigações funcionaram**. Os testes demonstram claramente a diferença entre o estado vulnerável e o estado protegido da aplicação.

### 🔍 Teste de SSRF (Bloqueado)
```bash
# ✅ URL permitida (deve funcionar)
curl "http://localhost:5000/predict?image_url=https://i.imgur.com/image.jpg"

# ❌ URL bloqueada (deve retornar 403)
curl "http://localhost:5000/predict?image_url=http://127.0.0.1:8080/admin"
```
**Resultado**: O curl da URL bloqueada agora retorna **403 Forbidden**, impedindo acesso a recursos internos.

### 🚫 Teste de DoS (Rate Limiting)
```bash
# Teste de limite de requisições
for i in {1..15}; do
  curl "http://localhost:5000/predict?image_url=https://i.imgur.com/image.jpg"
  echo "Requisição $i"
done
# Após 10 requisições: 429 Too Many Requests
```
**Resultado**: O teste de rajada agora resulta em **429 Too Many Requests** após exceder o limite de 10 requisições por minuto.

### 📊 Monitoramento
```bash
# Logs da aplicação
tail -f app.log

# Monitorar recursos
htop
```

## 📊 Arquitetura e Resiliência (Defesa em Profundidade)

### 🎯 Ataques Identificados
Para visualizar os diagramas detalhados de cada tipo de ataque, consulte:
- **[📊 Security Attack Flowcharts](sprint4_app/security_attack_flowcharts.md)**

### 🛡️ Arquitetura de Proteção
A arquitetura implementada segue o princípio de **defesa em profundidade**:

1. **WAF** - Filtro inicial de tráfego
2. **Rate Limiter** - Controle de requisições
3. **Validador URL** - Prevenção de SSRF
4. **Backup Service** - Resiliência contra ransomware

### 🔒 Resiliência contra Ransomware
Para o Ransomware, a solução é a **Resiliência Arquitetônica** baseada em Backups. O diagrama final ilustra esse princípio, mostrando como o sistema de backup externo protege contra a criptografia de arquivos críticos, garantindo a recuperação mesmo em caso de ataque bem-sucedido.

## 📚 Recursos

### 🔗 Links Úteis
- **[OWASP Top 10](https://owasp.org/www-project-top-ten/)** - Top 10 vulnerabilidades web
- **[Flask Security](https://flask.palletsprojects.com/en/2.3.x/security/)** - Boas práticas de segurança
- **[Mermaid Diagrams](https://mermaid.js.org/syntax/flowchart.html)** - Sintaxe dos diagramas

### 📖 Documentação Técnica
- **[Security Flowcharts](sprint4_app/security_attack_flowcharts.md)** - Diagramas detalhados
- **[API Documentation](#-endpoints)** - Documentação dos endpoints
- **[Test Cases](#-testes-de-segurança)** - Casos de teste de segurança

### 🛠️ Tecnologias Utilizadas
| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **Python** | 3.7+ | Linguagem principal |
| **Flask** | 2.0+ | Framework web |
| **Flask-Limiter** | Latest | Rate limiting |
| **Mermaid** | Latest | Diagramas |

## ⚠️ Aviso de Segurança

> **🚨 IMPORTANTE**: Esta aplicação contém vulnerabilidades intencionais para fins educacionais. 
> 
> **NÃO utilize em ambiente de produção** sem implementar as devidas mitigações de segurança.

### 🔒 Considerações de Segurança
- ✅ **Educacional**: Apenas para aprendizado
- ❌ **Produção**: Não recomendado para uso real
- 🛡️ **Mitigações**: Implementadas para demonstração
- 📚 **Objetivo**: Conscientização sobre segurança

---

<div align="center">

### 🎓 **Projeto Educacional - FIAP**
**Sprint 4 - Análise de Vulnerabilidades de Segurança**

[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/9luis7/sprint4-secure-ml-app)
[![Python](https://img.shields.io/badge/Python-3.7+-blue?style=for-the-badge&logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)

</div>
