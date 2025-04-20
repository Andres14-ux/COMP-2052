from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/libros")
def libros():
    lista_libros = [
        {"titulo": "Como agua para chocolate"},
        {"titulo": "Don Quijote de la Mancha"},
        {"titulo": "La Sombra del Viento"},
        {"titulo": "Cien años de soledad"},
        {"titulo": "El tunel"},
        {"titulo": "Marianela"}
    ]   
    return render_template("libros.html", libros=lista_libros)

@app.route("/autores")
def autores():
    lista_autores = ["Gabriel García Márquez", "Miguel de Cervantes", "Carlos Ruiz Zafón", "Laura Esquivel", "Benito Pérez Galdós", "Ernesto Sabato"]
    return render_template("autores.html", autores=lista_autores)

if __name__ == "__main__":
    app.run(debug=True)
