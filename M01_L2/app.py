from flask import Flask, request, jsonify

app = Flask(__name__)

#Get
@app.route('/info', methods=['GET'])
def info():
    return jsonify({
        "nombre_aplicacion": "Capstone Flask API",
        "version": "1.0",
        "descripcion": "Esta aplicacion demuestra una arquitectura Cliente/Servidor con Flask y se demostrara esta informacion."
    })

#Post
@app.route('/mensaje', methods=['GET','POST'])
def mensaje():
    if request.method == 'POST':
        datos = request.get_json()
        mensaje = datos.get("mensaje")
        if not mensaje:
            return jsonify({"error": "El campo 'mensaje' es requerido."}), 400
        return jsonify({"respuesta": f"Mensaje recibido: {mensaje}"}), 200
    else:
        return jsonify({"info": "En esta ruta se vera el POST."})
  

if __name__ == '__main__':
    app.run(debug=True)
