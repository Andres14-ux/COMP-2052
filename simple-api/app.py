from flask import Flask, jsonify, request

app = Flask(__name__)

todos = {
    "todos": ['Estudiar', 'Comer', 'Jugar UNO']
    }

@app.route("/", methods=["GET"])
def home():
    return "Simple TODO API"

@app.route("/todos", methods=["GET"])
def select_todos():
    return jsonify(todos)

@app.route("/todos", methods=["POST"])
def create_todo():
    data = request.json
    if not data or "todo" not in data:
        return jsonify({"error": "Datos incompletos"}), 400
    
    todos ["todos"].append(data['todo'])

    return jsonify({"message": "Nuevo todo creado"}), 200


if __name__ == "__main__":
    app.run(debug=True)