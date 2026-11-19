import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    # Só na própria máquina. Para ativar o modo debug: FLASK_DEBUG=1
    app.run(host="127.0.0.1", port=5000, debug=os.getenv("FLASK_DEBUG") == "1")
