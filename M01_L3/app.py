from flask import Flask, jsonify, request

app = Flask(__name__)

# Lista para almacenar usuarios
usuarios = []

# GET
@app.route('/info', methods=['GET'])
def info():
    return jsonify({
        'nombre_sistema': 'Gestor de Usuarios',
        'version': '1.0',
        'descripcion': 'Sistema básico para gestión de usuarios con Flask'
    })

# POST
@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    datos = request.get_json()
    nombre = datos.get('nombre')
    correo = datos.get('correo')

    if not nombre or not correo:
        return jsonify({'error': 'Faltan datos. Se requiere "nombre" y "correo".'}), 400

    usuario = {'nombre': nombre, 'correo': correo}
    usuarios.append(usuario)

    return jsonify({'mensaje': 'Usuario creado con éxito', 'usuario': usuario}), 201

# GET usuarios
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    return jsonify({'usuarios': usuarios})

if __name__ == '__main__':
    app.run(debug=True)
