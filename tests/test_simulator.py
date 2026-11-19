import pytest

from app import create_app

import app.utils as utils
from app.utils import TargetNotAllowed, try_passwords, validate_target
from target_server import LAB_PASSWORD, LAB_USER, create_target_app


@pytest.fixture
def lab(monkeypatch):
    """Liga o simulador ao servidor-alvo de teste, sem abrir rede de verdade."""

    def attach(lockout_after=0):
        client = create_target_app(lockout_after).test_client()

        class Resposta:
            def __init__(self, resp):
                self.status_code = resp.status_code
                self._resp = resp

            def json(self):
                return self._resp.get_json()

        monkeypatch.setattr(
            utils.requests, "post", lambda url, data, timeout: Resposta(client.post("/login", data=data))
        )

    return attach


WORDS = ["123456", "senha", LAB_PASSWORD, "outra"]
URL = "http://localhost:5001/login"


def test_encontra_a_senha_fraca(lab):
    lab()
    result = try_passwords(LAB_USER, URL, WORDS)
    assert result.startswith("SUCESSO")
    assert LAB_PASSWORD in result
    assert "tentativa 3" in result


def test_nao_encontra_quando_a_senha_nao_esta_na_lista(lab):
    lab()
    assert try_passwords(LAB_USER, URL, ["a", "b"]).startswith("Nenhuma")


def test_o_bloqueio_de_conta_para_o_ataque(lab):
    lab(lockout_after=2)
    result = try_passwords(LAB_USER, URL, WORDS)
    assert result.startswith("BLOQUEADO")
    assert "3 tentativa" in result


@pytest.mark.parametrize(
    "url",
    ["http://example.com/login", "https://192.168.0.10/login", "ftp://localhost/x", "http://localhost.evil.com/", ""],
)
def test_recusa_alvos_fora_da_maquina_local(url):
    with pytest.raises(TargetNotAllowed):
        validate_target(url)


@pytest.mark.parametrize("url", ["http://localhost:5001/login", "http://127.0.0.1:5001/login", "http://[::1]:5001/login"])
def test_aceita_alvos_locais(url):
    assert validate_target(url) == url


def test_try_passwords_nao_dispara_requisicao_para_alvo_externo(monkeypatch):
    def nunca(*args, **kwargs):
        raise AssertionError("não deveria ter feito requisição")

    monkeypatch.setattr(utils.requests, "post", nunca)
    assert try_passwords("x", "http://example.com/login", ["a"]).startswith("Erro")


def test_lista_de_exemplo_acompanha_o_projeto_e_tem_a_senha_do_laboratorio():
    exemplo = utils.EXAMPLE_WORDLIST_PATH.read_text(encoding="utf-8").split()
    assert LAB_PASSWORD in exemplo


def test_pagina_do_simulador_abre_e_recusa_alvo_externo(monkeypatch):
    monkeypatch.setenv("TARGET_URL", "http://example.com/login")
    client = create_app().test_client()
    assert client.get("/").status_code == 200
    resposta = client.post("/", data={"username": "admin"})
    assert "só aceita alvos em localhost" in resposta.get_data(as_text=True)
