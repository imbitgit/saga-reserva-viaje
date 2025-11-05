from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

SERVICES = [
    ("user", "http://user_service_james:5101"),
    ("cart", "http://cart_service:5102"),
    ("inventory", "http://inventory_service:5103"),
    ("payment", "http://payment_service:5104"),
    ("invoice", "http://invoice_service:5105"),
    ("shipping", "http://shipping_service:5106"),
    ("notification", "http://notification_service:5107"),
    ("analytics", "http://analytics_service:5108"),
    ("loyalty", "http://loyalty_service:5109"),
    ("review", "http://review_service:5110")
]

@app.route('/process-order', methods=['POST'])
def process_order():
    user = request.json.get("user")
    successful = []

    try:
        for name, url in SERVICES:
            print(f"🚀 Ejecutando {name} para {user}")
            r = requests.post(f"{url}/reserve", json={"user": user})
            if r.status_code != 200:
                raise Exception(f"Falla en {name}")
            successful.append((name, url))

        return jsonify({"message": f"Orden completada exitosamente para {user}"}), 200

    except Exception as e:
        print(f"❌ Error: {e}")
        for name, url in reversed(successful):
            print(f"↩️ Compensando {name}")
            requests.post(f"{url}/cancel", json={"user": user})
        return jsonify({"message": f"Orden fallida para {user}. Se aplicaron compensaciones."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100)

