# Diagrama de Fluxo - Ataque SSRF (Server-Side Request Forgery)

## Vulnerabilidade Identificada
A aplicação Flask em `app.py` possui uma vulnerabilidade SSRF no endpoint `/predict` que aceita o parâmetro `image_url` sem validação adequada.

## Diagrama de Fluxo do Ataque

```mermaid
graph TD;
    subgraph "Internet"
        Attacker["🕵️ Atacante"];
    end

    subgraph "Infraestrutura do Servidor"
        WebApp["🖥️ Nosso App Web (Vulnerável)"];
        subgraph "Rede Interna (localhost)"
            AdminPanel["🗄️ Painel Admin Interno"];
        end
    end

    Attacker -- "1. Envia URL maliciosa: /predict?image_url=http://127.0.0.1/admin" --> WebApp;
    WebApp -- "2. Requisição Forjada (SSRF) - O App acessa o recurso interno" --> AdminPanel;

    style Attacker fill:#e74c3c,stroke:#c0392b,stroke-width:3px,color:#fff
    style WebApp fill:#f39c12,stroke:#e67e22,stroke-width:3px,color:#fff
    style AdminPanel fill:#3498db,stroke:#2980b9,stroke-width:3px,color:#fff
```

## Explicação do Ataque

1. **Atacante**: Envia uma requisição maliciosa para o endpoint `/predict` com uma URL interna como parâmetro
2. **Aplicação Web**: Processa a requisição sem validar se a URL é interna ou externa
3. **Painel Admin**: Recebe uma requisição que deveria ser bloqueada, mas é processada devido à vulnerabilidade SSRF

## Exemplo de Payload Malicioso
```
GET /predict?image_url=http://127.0.0.1:8080/admin
GET /predict?image_url=http://localhost:3306/mysql
GET /predict?image_url=file:///etc/passwd
```

## Mitigações Recomendadas
- Validar URLs permitidas (whitelist)
- Bloquear requisições para IPs internos
- Usar bibliotecas de validação de URL
- Implementar timeouts para requisições externas
- Monitorar logs de requisições suspeitas

---

# Diagrama de Fluxo - Ataque DoS (Denial of Service)

## Vulnerabilidade Identificada
A aplicação Flask pode ser sobrecarregada por múltiplas requisições simultâneas, causando esgotamento de recursos do servidor.

## Diagrama de Fluxo do Ataque DoS

```mermaid
graph TD;
    subgraph "Atacantes (Botnet)"
        direction LR
        Bot1["🤖 Bot 1"];
        Bot2["🤖 Bot 2"];
        Bot3["🤖 Bot 3"];
    end

    subgraph "Infraestrutura"
        WebApp["🖥️ Nosso App Web"];
        Resources["💾 Recursos Esgotados (CPU/RAM)"];
    end

    User["👤 Usuário Legítimo"];

    Bot1 & Bot2 & Bot3 -- "1. Requisições em Massa" --> WebApp;
    WebApp -- "2. Sobrecarga" --> Resources;
    User -.->|"3. Acesso Negado!"| WebApp;

    style Bot1 fill:#e74c3c,stroke:#c0392b,stroke-width:3px,color:#fff
    style Bot2 fill:#e74c3c,stroke:#c0392b,stroke-width:3px,color:#fff
    style Bot3 fill:#e74c3c,stroke:#c0392b,stroke-width:3px,color:#fff
    style User fill:#27ae60,stroke:#229954,stroke-width:3px,color:#fff
```

## Explicação do Ataque DoS

1. **Botnet**: Múltiplos bots coordenados enviam requisições simultâneas
2. **Aplicação Web**: Tenta processar todas as requisições simultaneamente
3. **Recursos Esgotados**: CPU e RAM são sobrecarregados
4. **Usuário Legítimo**: Não consegue acessar o serviço devido à sobrecarga

## Exemplo de Ataque
- **Requisições simultâneas**: 1000+ requisições por segundo
- **Recursos afetados**: CPU 100%, RAM esgotada
- **Resultado**: Serviço indisponível para usuários legítimos

## Mitigações Recomendadas para DoS
- Implementar rate limiting (limite de requisições por IP)
- Usar CDN para distribuir carga
- Configurar load balancers
- Implementar cache para reduzir processamento
- Monitorar métricas de performance
- Configurar timeouts adequados
- Usar ferramentas de proteção como Cloudflare

---

# Diagrama de Fluxo - Ataque de Ransomware

## Vulnerabilidade Identificada
A aplicação Flask pode ser comprometida através de vulnerabilidades que permitem execução de código malicioso, resultando em criptografia de arquivos críticos.

## Diagrama de Fluxo do Ataque de Ransomware

```mermaid
graph TD;
    Attacker["🕵️ Atacante"] --> Exploit["1. Explora Vulnerabilidade no Servidor"];
    Exploit --> Server["🖥️ Servidor da Aplicação"];
    Attacker -->|"2. Injeta Payload"| Ransomware["💀 Malware Ransomware"];
    Ransomware -->|"3. Executa no"| Server;

    subgraph "Arquivos no Servidor"
        direction LR
        AppFile["📄 app.py"];
        ModelFile["🧠 model.pkl"];
    end

    Server --> Ransomware;
    Ransomware -- "4. Criptografa Arquivos" --> AppFile & ModelFile;

    subgraph "Resultado do Ataque"
        direction LR
        EncryptedApp["🔒 app.py.locked"];
        EncryptedModel["🔒 model.pkl.locked"];
    end
    
    AppFile --> EncryptedApp;
    ModelFile --> EncryptedModel;

    style Attacker fill:#e74c3c,stroke:#c0392b,stroke-width:3px,color:#fff
    style Ransomware fill:#8e44ad,stroke:#7d3c98,stroke-width:3px,color:#fff
    style EncryptedApp fill:#34495e,stroke:#2c3e50,stroke-width:3px,color:#fff
    style EncryptedModel fill:#34495e,stroke:#2c3e50,stroke-width:3px,color:#fff
```

## Explicação do Ataque de Ransomware

1. **Atacante**: Explora vulnerabilidades no servidor (SSRF, DoS, ou outras)
2. **Exploração**: Obtém acesso ao sistema através de falhas de segurança
3. **Injeção de Payload**: Instala malware ransomware no servidor
4. **Execução**: O ransomware executa no servidor comprometido
5. **Criptografia**: Arquivos críticos são criptografados e tornados inutilizáveis

## Arquivos Afetados na Aplicação
- **app.py**: Código principal da aplicação Flask
- **model.pkl**: Modelo de machine learning carregado pela aplicação
- **Outros arquivos**: Dados, logs, configurações

## Consequências do Ataque
- **Aplicação indisponível**: Arquivos criptografados impedem execução
- **Perda de dados**: Modelo de ML e código fonte inacessíveis
- **Paralisação do serviço**: Sistema completamente comprometido
- **Pedido de resgate**: Atacante exige pagamento para descriptografar

## Exemplo de Vulnerabilidades que Podem Ser Exploradas
- **SSRF**: Para acessar recursos internos
- **DoS**: Para sobrecarregar e criar brechas
- **Injeção de código**: Através de parâmetros não validados
- **Upload de arquivos**: Se a aplicação permitir uploads

## Mitigações Recomendadas para Ransomware
- **Backups regulares**: Manter cópias seguras dos arquivos críticos
- **Atualizações de segurança**: Manter sistema e dependências atualizadas
- **Antivírus/Antimalware**: Proteção em tempo real
- **Princípio do menor privilégio**: Limitar permissões de usuários
- **Monitoramento**: Detectar atividades suspeitas
- **Segmentação de rede**: Isolar sistemas críticos
- **Treinamento**: Educar usuários sobre phishing e ameaças
- **Plano de recuperação**: Procedimentos para restaurar após ataque

---

# Diagrama de Fluxo - Arquitetura Final Segura

## Arquitetura de Segurança Implementada
A aplicação agora possui múltiplas camadas de proteção contra os ataques identificados, formando uma arquitetura de segurança robusta.

## Diagrama de Fluxo da Arquitetura Segura

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

    AppServer -- "Backups Regulares" --> BackupService;

    style User fill:#27ae60,stroke:#229954,stroke-width:3px,color:#fff
    style WAF fill:#3498db,stroke:#2980b9,stroke-width:3px,color:#fff
    style RateLimiter fill:#f39c12,stroke:#e67e22,stroke-width:3px,color:#fff
    style URLValidator fill:#e74c3c,stroke:#c0392b,stroke-width:3px,color:#fff
```

## Explicação da Arquitetura de Segurança

### 1. **WAF (Web Application Firewall) - Primeira Camada**
- **Função**: Filtro inicial de tráfego malicioso
- **Proteção**: Bloqueia ataques conhecidos antes de chegar à aplicação
- **Benefícios**: Reduz carga na aplicação e protege contra vulnerabilidades

### 2. **Rate Limiter (Anti-DoS) - Segunda Camada**
- **Implementação**: Flask-Limiter
- **Limite**: 10 requisições por minuto por IP
- **Proteção**: Previne sobrecarga do servidor
- **Resposta**: 429 Too Many Requests quando exceder limite

### 3. **Validador de URL (Anti-SSRF) - Terceira Camada**
- **Implementação**: Validação de domínios permitidos
- **Whitelist**: `i.imgur.com`, `images.pexels.com`
- **Proteção**: Bloqueia acesso a recursos internos
- **Resposta**: 403 Forbidden para URLs não permitidas

### 4. **Modelo de ML - Processamento Seguro**
- **Função**: Processamento de predições
- **Proteção**: Executado apenas após todas as validações
- **Carga**: Simulação com `time.sleep(0.5)`

### 5. **Serviço de Backup - Resiliência**
- **Função**: Backup regular dos arquivos críticos
- **Proteção**: Recuperação contra ataques de ransomware
- **Frequência**: Backups automáticos e regulares

## Fluxo de Segurança

1. **Usuário/Atacante** → Requisição para aplicação
2. **WAF** → Filtro inicial de segurança
3. **Rate Limiter** → Verificação de limite de requisições
4. **Validador de URL** → Validação de domínios permitidos
5. **Modelo de ML** → Processamento seguro da predição
6. **Backup Service** → Proteção contra ransomware

## Benefícios da Arquitetura

### **Defesa em Profundidade**
- Múltiplas camadas de proteção
- Falha de uma camada não compromete o sistema
- Redundância de segurança

### **Proteção Específica**
- **SSRF**: Validação de URLs + WAF
- **DoS**: Rate limiting + WAF
- **Ransomware**: Backups regulares + WAF

### **Monitoramento**
- Logs detalhados em cada camada
- Detecção de tentativas de ataque
- Métricas de performance e segurança

## Implementações Realizadas

### ✅ **Proteções Ativas**
- Rate limiting com Flask-Limiter
- Validação de domínios para SSRF
- Simulação de carga de trabalho
- Estrutura para backups

### 🔄 **Melhorias Futuras**
- Implementação de WAF real
- Sistema de backup automatizado
- Monitoramento avançado
- Alertas de segurança