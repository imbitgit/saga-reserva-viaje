from flask import Flask, request, jsonify
import random

app = Flask(__name__)
data = []

@app.route('/reserve', methods=['POST'])
def reserve():
    user = request.json.get('user')
    # Simular falla aleatoria (10%)
    if random.random() < 0.1:
        return jsonify({"message": f"Error en user_service con {user}"}), 500
    data.append(user)
    return jsonify({"message": f"user_service completado para {user}"}), 200

@app.route('/cancel', methods=['POST'])
def cancel():
    user = request.json.get('user')
    if user in data:
        data.remove(user)
        return jsonify({"message": f"user_service compensado para {user}"}), 200
    return jsonify({"message": f"Sin datos para {user}"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5101)

