from flask import Flask, request, jsonify

app = Flask(__name__)

# Base de datos en memoria de estudiantes con varita validada
validated_wands = []

@app.route('/validate', methods=['POST'])
def validate_wand():
    data = request.json
    student = data.get('student')
    
    if student in validated_wands:
        return jsonify({"message": f"Varita ya validada para {student}"}), 200

    # Registrar la varita como validada
    validated_wands.append(student)
    return jsonify({"message": f"Varita validada y lista para {student}"}), 200

@app.route('/revoke', methods=['POST'])
def revoke_wand():
    data = request.json 
    student = data.get('student')
    
    # Lógica de compensación: anular la validación
    if student in validated_wands:
        validated_wands.remove(student)
        return jsonify({"message": f"Validación de varita anulada para {student}"}), 200
    else:
        return jsonify({"message": f"No hay validación de varita activa para {student}"}), 404

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify(validated_wands), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)