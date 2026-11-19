"""Servidor-alvo de laboratório: o "sistema" que o simulador tenta invadir.

Roda só em 127.0.0.1. Existe um único usuário de teste e uma senha fraca de propósito.
Por padrão não tem nenhuma defesa. Com LOCKOUT_AFTER=5, trava o usuário depois de 5 erros seguidos.

    python target_server.py                   # sem defesa
    LOCKOUT_AFTER=5 python target_server.py   # com bloqueio de conta
"""
import os

from flask import Flask, jsonify, request

LAB_USER = "admin"
LAB_PASSWORD = "laboratorio2024"  # senha fraca, só para o experimento
LOCKOUT_AFTER = int(os.getenv("LOCKOUT_AFTER", "0"))  # 0 = sem bloqueio


def create_target_app(lockout_after=LOCKOUT_AFTER):
    app = Flask(__name__)
    failures = {}

    @app.post("/login")
    def login():
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if lockout_after and failures.get(username, 0) >= lockout_after:
            return jsonify(authenticated=False, locked=True), 429

        if username == LAB_USER and password == LAB_PASSWORD:
            failures[username] = 0
            return jsonify(authenticated=True)

        failures[username] = failures.get(username, 0) + 1
        return jsonify(authenticated=False), 401

    return app


if __name__ == "__main__":
    modo = f"bloqueio após {LOCKOUT_AFTER} erros" if LOCKOUT_AFTER else "sem defesa"
    print(f"Servidor-alvo em http://127.0.0.1:5001/login ({modo}). Usuário de teste: {LAB_USER}")
    create_target_app().run(host="127.0.0.1", port=5001)
