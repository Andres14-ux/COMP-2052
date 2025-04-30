from flask import Flask, request, jsonify

app = Flask(__name__)

#Lista en memoria para almacenar usuarios
usuarios = ['Jose', 'Maria', 'Pedro']

#Get info
@app.route('/info', methods=['GET'])
def info():
    return jsonify({
        "sistema": "Gestion de usuarios",
        "version": "1.0",
        "descripcion": "Esta app es para registrar y listar usuarios usando Flask."
    })

#Post usuario
@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    datos = request.get_json()

    nombre = datos.get('nombre')
    correo = datos.get('correo')

    if not nombre or not correo:
        return jsonify({
            "error": "Faltan datos. Se requiere 'nombre' y 'correo'."
        }), 400

    nuevo_usuario = {"nombre": nombre, "correo": correo}
    usuarios.append(nuevo_usuario)

    return jsonify({
        "mensaje": "Usuario creado con exito.",
        "usuario": nuevo_usuario
    }), 201

#Get usuarios
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    return jsonify({
        "mensaje": "Lista de usuarios",
        "usuarios": usuarios
    })

if __name__ == '__main__':
    app.run(debug=True)
