from flask import Flask, request, jsonify

app = Flask(__name__)

# Guardar usuarios
usuarios = []

# Ruta GET /info
@app.route("/info", methods=["GET"])
def info():
    return jsonify({
        "sistema": "Gestión de Usuarios y Productos",
        "versión": "1.0",
        "autor": "Andres  M Tosado"
    })

# Ruta POST /crear_usuario
@app.route("/crear_usuario", methods=["POST"])
def crear_usuario():
    datos = request.get_json()

    # Validación de datos
    nombre = datos.get("nombre")
    correo = datos.get("correo")

    if not nombre or not correo:
        return jsonify({"error": "El nombre y el correo son requeridos."}), 400

    # Agregar usuario a la lista
    usuario = {"nombre": nombre, "correo": correo}
    usuarios.append(usuario)

    return jsonify({
        "mensaje": "Usuario creado exitosamente.",
        "usuario": usuario
    }), 201

# Ruta GET /usuarios
@app.route("/usuarios", methods=["GET"])
def obtener_usuarios():
    return jsonify({
        "cantidad": len(usuarios),
        "usuarios": usuarios
    })

# Ejecutar servidor
if __name__ == "__main__":
    app.run(debug=True)
