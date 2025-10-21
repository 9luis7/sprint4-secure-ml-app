from flask import Flask, request, jsonify
import joblib
import requests
import time
from urllib.parse import urlparse
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initialize Flask app
app = Flask(__name__)

# Proteção DoS: Rate Limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10 per minute"],
    storage_uri="memory://"
)

# Load model.pkl into global variable model before any request
model = joblib.load('model.pkl')

# Proteção SSRF: Domínios permitidos
ALLOWED_DOMAINS = {'i.imgur.com', 'images.pexels.com'}

@app.route('/predict', methods=['GET'])
@limiter.limit("10/minute")
def predict():
    # Simular carga de trabalho pesada
    time.sleep(0.5)
    
    # Extract image_url query parameter
    image_url = request.args.get('image_url')
    
    # Return 400 error if image_url is missing
    if not image_url:
        return jsonify({'error': 'image_url parameter is required'}), 400
    
    # Proteção SSRF: Validação de URL
    parsed_url = urlparse(image_url)
    
    # Verificar esquema (http/https)
    if parsed_url.scheme not in ['http', 'https']:
        return jsonify({'error': 'URL inválida ou não permitida.'}), 403
    
    # Verificar domínio permitido
    if parsed_url.netloc not in ALLOWED_DOMAINS:
        return jsonify({'error': 'URL inválida ou não permitida.'}), 403
    
    try:
        # PONTO DA VULNERABILIDADE: A aplicação faz uma requisição para a URL fornecida pelo usuário.
        response = requests.get(image_url, timeout=5)
        response.raise_for_status()  # Gera um erro para status HTTP 4xx/5xx
        print(f"SUCESSO AO ACESSAR URL. Status: {response.status_code}. Conteúdo: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"ERRO ao tentar acessar a URL: {e}")
    
    # Use loaded model to simulate prediction
    prediction = model['prediction']
    confidence = model['confidence']
    
    # Return JSON response with prediction and processed_url
    return jsonify({
        'prediction': prediction,
        'confidence': confidence,
        'processed_url': image_url
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
