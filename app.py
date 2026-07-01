import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# CONFIGURAÇÕES
DIFY_API_URL = "https://api.dify.ai/v1/chat-messages"
DIFY_API_KEY = "app-Akh9PYeeurIE4J8bcYzqAIcx" # A que você gerou lá

@app.route('/chat', methods=['POST'])
def chat():
    # O Vapi envia o JSON com a estrutura 'message' -> 'content'
    data = request.json
    try:
        user_message = data['message']['content']
    except KeyError:
        return jsonify({"error": "Formato inválido"}), 400
    
    # Payload para o Dify
    payload = {
        "inputs": {},
        "query": user_message,
        "response_mode": "blocking",
        "user": "vapi_user"
    }
    
    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}", 
        "Content-Type": "application/json"
    }
    
    # Chama o Dify
    try:
        response = requests.post(DIFY_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        dify_data = response.json()
        ai_response = dify_data.get("answer", "Desculpe, não consegui processar sua fala.")
    except Exception as e:
        ai_response = "Erro de conexão com o cérebro da Kaori."
    
    # Formato de resposta obrigatório para o Vapi
    return jsonify({
        "message": {
            "role": "assistant",
            "content": ai_response
        }
    })

if __name__ == '__main__':
    # O Render usa a porta definida pelo sistema
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
