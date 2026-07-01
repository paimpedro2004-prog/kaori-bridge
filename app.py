import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# CONFIGURAÇÕES
DIFY_API_URL = "https://api.dify.ai/v1/chat-messages"
DIFY_API_KEY = "app-Akh9PYeeurIE4J8bcYzqAIcx" 

def process_chat_request(data):
    # Extrai a mensagem enviada pelo usuário
    try:
        user_message = data['message']['content']
    except (KeyError, TypeError):
        return jsonify({"message": {"role": "assistant", "content": "Erro: formato de mensagem inválido."}}), 400
    
    # Payload para o Dify
    payload = {
        "inputs": {},
        "query": user_message,
        "response_mode": "blocking",
        "user": "vapi_kaori_user"
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
        ai_response = dify_data.get("answer", "...")
    except Exception as e:
        ai_response = "Desculpe, estou com problemas técnicos no momento."
    
    return jsonify({
        "message": {
            "role": "assistant",
            "content": ai_response
        }
    })

# Rota original
@app.route('/chat', methods=['POST'])
def chat():
    return process_chat_request(request.json)

# Rota de resgate para o caminho forçado pelo Vapi
@app.route('/chat/chat/completions', methods=['POST'])
def chat_completions_proxy():
    return process_chat_request(request.json)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
