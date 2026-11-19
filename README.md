# Brute Force Simulator

> **Projeto apenas para fins educativos.** Só ataca a sua própria máquina.

Laboratório que mostra, na prática, como um **ataque de dicionário** quebra uma senha fraca e como uma defesa simples
(bloqueio de conta) o para. O projeto tem duas partes:

- **o simulador** (Flask, porta 5000): testa cada senha de uma lista contra um alvo;
- **o servidor-alvo** (`target_server.py`, porta 5001): o "sistema" a ser atacado, com uma senha fraca de propósito e um
  bloqueio de conta que você liga ou desliga.

## O que o experimento mostra

**1. Sem defesa, uma senha fraca cai em segundos.** O alvo tem o usuário `admin` e uma senha comum de dicionário:

```text
[18] senha testada: 'admin123' -> HTTP 401
[19] senha testada: 'laboratorio2024' -> HTTP 200
SUCESSO: senha 'laboratorio2024' encontrada na tentativa 19.
```

**2. Com bloqueio de conta, o mesmo ataque para.** Ligando `LOCKOUT_AFTER=5`, o alvo trava o usuário depois de 5 erros:

```text
[5] senha testada: 'abc123' -> HTTP 401
[6] senha testada: '111111' -> HTTP 429
BLOQUEADO após 6 tentativa(s): o alvo travou a conta. Esta é a defesa funcionando.
```

### Defesas que o experimento sugere

| Defesa | O que faz |
|---|---|
| **Limite de tentativas / bloqueio** | Torna o ataque por dicionário inviável (o que o `LOCKOUT_AFTER` demonstra). |
| **Senhas fortes e únicas** | Tira a senha da lista de candidatas. A do laboratório é fraca de propósito. |
| **Hash lento (Argon2id, bcrypt)** | Se o banco vazar, cada tentativa offline custa caro. Veja o [password-hash-battle](https://github.com/Wellington-Barbosa/password-hash-battle). |
| **Segundo fator (MFA)** | Mesmo com a senha descoberta, falta o segundo passo. |
| **Registro e alerta** | Muitas falhas seguidas num usuário são um sinal claro de ataque. |

## Como executar

Requer Python 3.10 ou superior.

```bash
git clone https://github.com/Wellington-Barbosa/brute-force-simulator.git
cd brute-force-simulator
python -m venv venv
```

Ative o ambiente (Windows: `venv\Scripts\activate`; Linux e macOS: `source venv/bin/activate`) e instale:

```bash
pip install -r requirements.txt
```

Configure o alvo (aceita apenas endereços locais). No Windows, use `copy .env.example .env`:

```bash
cp .env.example .env
```

**Terminal 1: o servidor-alvo, sem defesa.**

```bash
python target_server.py
```

Para repetir o experimento com bloqueio de conta, pare o servidor e suba de novo com a defesa ligada
(no Windows, antes disso, rode `set LOCKOUT_AFTER=5`):

```bash
LOCKOUT_AFTER=5 python target_server.py
```

**Terminal 2: o simulador.**

```bash
python run.py
```

Abra [http://localhost:5000](http://localhost:5000), informe o usuário `admin` e clique em **Processar**. O resultado aparece
na página e cada tentativa é impressa no terminal.

A lista de senhas padrão é `wordlist/wordlist.example.txt`. Para usar a sua, crie `wordlist/wordlist.txt`
(o arquivo não é versionado e tem prioridade sobre o de exemplo).

## Segurança do próprio simulador

- **Só aceita alvos locais.** Qualquer `TARGET_URL` fora de `localhost`, `127.0.0.1` ou `::1` é recusado antes de qualquer
  requisição. O comportamento está coberto por testes.
- Tem tempo-limite por requisição e, por padrão, não roda em modo debug.
- O servidor-alvo escuta só em `127.0.0.1`. Não o exponha na rede.

## Estrutura

```text
brute-force-simulator/
├── app/
│   ├── __init__.py          # app Flask do simulador
│   ├── routes.py            # página com o formulário
│   └── utils.py             # try_passwords(), validação do alvo e leitura da lista
├── target_server.py         # alvo de laboratório, com bloqueio de conta opcional
├── wordlist/
│   └── wordlist.example.txt # lista de exemplo (19 senhas comuns)
├── tests/                   # testes (pytest)
├── .env.example             # modelo de configuração
├── requirements.txt
└── run.py                   # inicia o simulador
```

## Testes

```bash
pip install pytest
pytest
```

Os testes cobrem: senha encontrada, lista sem a senha, bloqueio de conta e a recusa de alvos fora da máquina local.

## Aviso legal

Este código é fornecido **exclusivamente para estudo e pesquisa**. **Nunca** use contra sistemas sem autorização explícita:
isso pode violar a lei e resultar em penalidades civis e criminais. Você é integralmente responsável pelo uso.

## Contato

Sugestões ou melhorias? Abra uma [issue](https://github.com/Wellington-Barbosa/brute-force-simulator/issues) ou envie um Pull Request.
