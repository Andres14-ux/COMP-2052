from flask import Flask, request, jsonify

app = Flask(__name__)

# Ruta GET
@app.route("/info", methods=["GET"])
def info():
    return jsonify({
        "nombre": "Proyecto Capstone",
        "versión": "1.0",
        "autor": "Andrés  M Tosado"
    })

# Ruta POST
@app.route("/mensaje", methods=["POST"])
def mensaje():
    datos = request.get_json()
    texto = datos.get("mensaje", "Sin mensaje recibido")
    return jsonify({
        "respuesta": f"Recibí tu mensaje: {texto}"
    })

if __name__ == "__main__":
    app.run(debug=True)
