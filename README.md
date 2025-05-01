# 🛡️ Brute Force Simulator

> ⚠️ **Projeto apenas para fins educativos e de estudo.**

Simulador de força bruta de login, desenvolvido para demonstrar como ataques de dicionário funcionam em ambiente controlado. Ideal para aprendizado em segurança da informação e testes éticos.

---

## ⚠️ Aviso Legal

Este código é fornecido **exclusivamente para fins de estudo e pesquisa**.  
**NUNCA** use este simulador contra sistemas sem autorização explícita.  
O uso indevido pode violar leis locais e resultar em **penalidades civis e criminais**.

---

## 📁 Estrutura do Projeto

```
brute-force-simulator/
├── app/
│   ├── __init__.py           → Inicialização do app Flask
│   ├── routes.py             → Rota principal com formulário de login
│   └── utils.py              → Função de força bruta usando wordlist
├── wordlist/
│   └── wordlist.txt          → Lista de senhas a serem testadas
├── .env                      → Define TARGET_URL do servidor-alvo
├── requirements.txt          → Dependências do projeto
├── run.py                    → Inicializa o servidor Flask
└── venv/                     → Ambiente virtual (ignorado no Git)
```

---

## 🚀 Como Executar o Projeto

1. **Clone o repositório:**

```bash
    git clone https://github.com/seu-usuario/brute-force-simulator.git
    cd brute-force-simulator
```

2. **Crie e ative o ambiente virtual:**

```bash
    python -m venv venv
```

**Ative conforme seu sistema:**

- **Windows:**
  ```bash
  venv\Scripts\activate
  ```

- **Linux/macOS:**
  ```bash
  source venv/bin/activate
  ```

3. **Instale as dependências:**

```bash
    pip install -r requirements.txt
```

4. **Configure o arquivo `.env` com o endpoint de teste:**

```bash
    echo TARGET_URL=http://localhost:5001/login > .env
```

5. **Execute o servidor Flask:**

```bash
    python run.py
```

Acesse no navegador: [http://localhost:5000](http://localhost:5000)

---

## 🧪 Funcionamento

- O formulário da interface permite o envio de um nome de usuário.
- A função `try_passwords()` testa senhas da `wordlist` via POST no `TARGET_URL`.
- Um login é considerado bem-sucedido se o retorno JSON for:

```json
{
  "authenticated": true
}
```

---

## 🛑 Termos de Uso

Este projeto é distribuído com o único propósito de **ensino e testes em ambientes controlados**.  
**Você é integralmente responsável pelo uso do código.**

---

## 📫 Contato

Sugestões ou melhorias?  
Abra uma [issue](https://github.com/seu-usuario/brute-force-simulator/issues) ou envie um **Pull Request**.  

Feliz hacking ético! 👨‍💻👩‍💻
