from flask import Flask, request, jsonify

app = Flask(__name__)

# Base de datos en memoria de estudiantes que recibieron su lechuza
delivered_owls = []

@app.route('/deliver', methods=['POST'])
def deliver_owl():
    data = request.json
    student = data.get('student')
    
    # Lógica de confirmación: enviar lechuza
    delivered_owls.append(student)
    return jsonify({"message": f"Lechuza de bienvenida enviada a {student}"}), 200

@app.route('/revoke', methods=['POST'])
def revoke_owl():
    data = request.json
    student = data.get('student')
    
    # Lógica de compensación: revocar la lechuza 
    if student in delivered_owls:
        delivered_owls.remove(student)
        return jsonify({"message": f"Lechuza de bienvenida revocada para {student}"}), 200
    else:
        return jsonify({"message": f"No hay lechuza enviada para {student}"}), 404

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify(delivered_owls), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)