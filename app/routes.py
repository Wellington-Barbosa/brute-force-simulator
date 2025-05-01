from flask import Blueprint, render_template_string, request
from .utils import try_passwords

main = Blueprint('main', __name__)

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login Brute Force Simulator</title>
</head>
<body>
    <h2>Simulador de Tentativas</h2>
    <form method="POST">
        <label>Usuário:</label>
        <input type="text" name="username" required />
        <button type="submit">Processar</button>
    </form>
    {% if result %}
        <p><strong>{{ result }}</strong></p>
    {% endif %}
</body>
</html>
"""

@main.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        username = request.form.get('username')
        result = try_passwords(username)
    return render_template_string(TEMPLATE, result=result)
