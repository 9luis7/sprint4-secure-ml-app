# Sprint 4 - Aplicação Flask com Análise de Vulnerabilidades de Segurança

## 📋 Visão Geral
Este projeto contém uma aplicação Flask de machine learning com vulnerabilidades de segurança intencionais para fins educacionais. O objetivo é demonstrar diferentes tipos de ataques cibernéticos e suas mitigações.

## 👥 Integrantes do Projeto
- **Luis Fernando de Oliveira Salgado** (RM: 561401)
- **Bernardo Braga Perobeli** (RM: 562468)
- **Lucca Phelipe Masini** (RM: 564121)
- **Igor Paixão Sarak** (RM: 563726)

## 🏗️ Estrutura do Projeto
```
CS/
├── sprint4_app/
│   ├── app.py                 # Aplicação Flask principal (VULNERÁVEL)
│   ├── create_model.py        # Script para criar modelo ML
│   ├── internal_service.py    # Serviço interno simulado (porta 8080)
│   ├── security_attack_flowcharts.md  # Diagramas de ataques
│   └── requirements.txt       # Dependências Python
└── README.md                  # Este arquivo
```

## 🚀 Como Executar

### Pré-requisitos
- Python 3.7+
- pip (gerenciador de pacotes Python)

### Instalação
```bash
# Navegar para o diretório da aplicação
cd sprint4_app

# Instalar dependências
pip install -r requirements.txt

# Executar a aplicação principal (VULNERÁVEL)
python app.py
```

### Executar Demonstração de Ataque SSRF
```bash
# Navegar para o diretório da aplicação
cd sprint4_app

# Terminal 1: Executar aplicação principal
python app.py

# Terminal 2: Executar serviço interno (em outro terminal)
python internal_service.py
```

### Acesso
- **Aplicação Principal**: http://localhost:5000
- **Serviço Interno**: http://localhost:8080
- **Endpoint vulnerável**: `/predict?image_url=<URL_DA_IMAGEM>`
- **Endpoint interno**: `/admin` (não deveria ser acessível externamente)

## 🚨 Vulnerabilidades Identificadas

### 1. SSRF (Server-Side Request Forgery) 🛡️ PROTEGIDO
- **Endpoint afetado**: `/predict`
- **Parâmetro vulnerável**: `image_url`
- **Proteção implementada**: Validação de domínios permitidos
- **Domínios permitidos**: `i.imgur.com`, `images.pexels.com`
- **Validações**: Esquema HTTP/HTTPS + Whitelist de domínios
- **Payload bloqueado**: `http://localhost:5000/predict?image_url=http://127.0.0.1:8080/admin`

### 2. DoS (Denial of Service) 🛡️ PROTEGIDO
- **Proteção implementada**: Rate limiting com Flask-Limiter
- **Limite**: 10 requisições por minuto por IP
- **Simulação**: `time.sleep(0.5)` em cada requisição
- **Risco**: Sobrecarga do servidor com requisições simultâneas
- **Impacto**: Indisponibilidade do serviço (agora protegido)

### 3. Ransomware
- **Vetor**: Exploração das vulnerabilidades anteriores
- **Alvo**: Arquivos críticos (`app.py`, `model.pkl`)
- **Consequência**: Criptografia e inutilização dos arquivos

## 📊 Diagramas de Segurança
- **[Security Attack Flowcharts](sprint4_app/security_attack_flowcharts.md)** - Diagramas Mermaid detalhando cada tipo de ataque

## 🛡️ Mitigações Recomendadas

### Para SSRF ✅ IMPLEMENTADO
- ✅ Validar URLs permitidas (whitelist) - `ALLOWED_DOMAINS`
- ✅ Bloquear requisições para IPs internos - Validação de domínio
- ✅ Implementar timeouts para requisições externas - `timeout=5`
- ✅ Validar esquemas HTTP/HTTPS apenas

### Para DoS ✅ IMPLEMENTADO
- ✅ **Rate limiting**: Flask-Limiter com 10 req/min por IP
- ✅ **Carga pesada simulada**: `time.sleep(0.5)` em cada requisição
- Usar CDN para distribuir carga
- Configurar load balancers

### Para Ransomware
- Backups regulares dos arquivos críticos
- Atualizações de segurança constantes
- Monitoramento de atividades suspeitas

## 🔧 Funcionalidades da Aplicação

### Endpoint `/predict`
- **Método**: GET
- **Parâmetros**: `image_url` (obrigatório)
- **Resposta**: JSON com predição e confiança do modelo
- **Exemplo**:
  ```bash
  curl "http://localhost:5000/predict?image_url=https://example.com/image.jpg"
  ```

## 📝 Logs e Monitoramento
- **SSRF Protegido**: A aplicação agora valida URLs antes de fazer requisições:
  - ✅ URLs permitidas: `i.imgur.com`, `images.pexels.com`
  - ❌ URLs bloqueadas: `localhost`, `127.0.0.1`, `file://`, etc.
  - 📝 Logs de sucesso: `"SUCESSO AO ACESSAR URL. Status: {status_code}. Conteúdo: {response_text}"`
  - 📝 Logs de erro: `"ERRO ao tentar acessar a URL: {erro}"`
- **DoS Protegido**: Rate limiting ativo com Flask-Limiter:
  - ✅ Limite: 10 requisições por minuto por IP
  - ❌ Bloqueio automático após exceder limite
  - 📝 Resposta de erro: `429 Too Many Requests`
- **Carga de Trabalho**: Cada requisição agora demora 0.5 segundos para simular processamento pesado
- **Serviço Interno**: Monitorar logs do `internal_service.py` para detectar acessos não autorizados
- **Recursos**: Observar uso de CPU/RAM para identificar ataques DoS (agora protegido)

## ⚠️ Aviso de Segurança
**ATENÇÃO**: Esta aplicação contém vulnerabilidades intencionais para fins educacionais. NÃO utilize em ambiente de produção sem implementar as devidas mitigações de segurança.

## 📚 Recursos Adicionais
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/2.3.x/security/)
- [Mermaid Diagram Syntax](https://mermaid.js.org/syntax/flowchart.html)

---
*Última atualização: $(date)*
