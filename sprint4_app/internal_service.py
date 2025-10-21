# internal_service.py
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/admin')
def admin_panel():
    """Este é o endpoint secreto que não deveria ser acessível de fora."""
    return jsonify({
        "message": "PAINEL DE ADMIN ACESSADO!",
        "secret_data": "chave_api_interna_12345"
    }), 200

if __name__ == '__main__':
    # Roda em uma porta diferente para não conflitar com nosso app principal
    app.run(port=8080, debug=True)
