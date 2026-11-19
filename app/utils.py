import os
from pathlib import Path
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
WORDLIST_PATH = BASE_DIR / "wordlist" / "wordlist.txt"
EXAMPLE_WORDLIST_PATH = BASE_DIR / "wordlist" / "wordlist.example.txt"

# Segurança: o simulador só ataca a própria máquina. Qualquer outro endereço é recusado.
ALLOWED_HOSTS = {"localhost", "127.0.0.1", "::1"}
REQUEST_TIMEOUT = 5  # segundos


class TargetNotAllowed(ValueError):
    """O endereço-alvo não é da máquina local."""


def validate_target(url):
    """Aceita apenas http(s) em localhost/127.0.0.1/::1. Levanta TargetNotAllowed nos demais casos."""
    if not url:
        raise TargetNotAllowed("TARGET_URL não definido. Copie .env.example para .env.")
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or parsed.hostname not in ALLOWED_HOSTS:
        raise TargetNotAllowed(
            "Por segurança, o simulador só aceita alvos em localhost, 127.0.0.1 ou ::1. "
            f"Recebido: {parsed.hostname or url!r}."
        )
    return url


def load_wordlist():
    """Usa wordlist/wordlist.txt se existir; senão, o exemplo que acompanha o projeto."""
    path = WORDLIST_PATH if WORDLIST_PATH.exists() else EXAMPLE_WORDLIST_PATH
    with open(path, encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]


def try_passwords(username, target_url=None, passwords=None):
    """Tenta cada senha da lista no alvo e devolve um resumo do resultado."""
    try:
        target = validate_target(target_url or os.getenv("TARGET_URL"))
        passwords = passwords if passwords is not None else load_wordlist()
    except (TargetNotAllowed, OSError) as error:
        return f"Erro: {error}"

    for attempt, password in enumerate(passwords, start=1):
        try:
            response = requests.post(
                target,
                data={"username": username, "password": password},
                timeout=REQUEST_TIMEOUT,
            )
        except requests.RequestException as error:
            return f"Erro ao falar com o alvo: {error}"

        print(f"[{attempt}] senha testada: {password!r} -> HTTP {response.status_code}")

        try:
            body = response.json()
        except ValueError:
            body = {}

        if response.status_code == 429 or body.get("locked") is True:
            return f"BLOQUEADO após {attempt} tentativa(s): o alvo travou a conta. Esta é a defesa funcionando."
        if body.get("authenticated") is True:
            return f"SUCESSO: senha {password!r} encontrada na tentativa {attempt}."

    return f"Nenhuma das {len(passwords)} senhas funcionou."
