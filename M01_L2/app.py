from flask import Flask, request, jsonify

app = Flask(__name__)

#GET
@app.route('/info', methods=['GET'])
def info():
    return jsonify({
        'nombre': 'Capstone Project API',
        'version': '1.0',
        'descripcion': 'API básica con Flask'
    })

#POST
@app.route('/mensaje', methods=['POST'])
def mensaje():
    datos = request.get_json()
    nombre = datos.get('nombre', 'invitado')
    return jsonify({'respuesta': f'Hola, {nombre}. ¡Tu mensaje fue recibido con éxito!'})

if __name__ == '__main__':
    app.run(debug=True)
