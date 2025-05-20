from flask import Blueprint, request, jsonify
from app.models import db, Curso

# Blueprint solo con endpoints de prueba para cursos
main = Blueprint('main', __name__)

@main.route('/') # Ambas rutas llevan al mismo lugar
@main.route('/dashboard')
def index():
    """
    Página de inicio pública (home).
    """
    return '<h1>Corriendo en Modo de Prueba.</h1>'

@main.route('/tickets', methods=['GET'])
def listar_tickets():
    """
    Retorna una lista de tickets (JSON).
    """
    tickets = tickets.query.all()

    data = [
        {'id': tickets.id, 'titulo': tickets.titulo, 'descripcion': tickets.descripcion, 'tecnico_id': tickets.tecnico_id}
        for ticket in tickets
    ]
    return jsonify(data), 200


@main.route('/tickets/<int:id>', methods=['GET'])
def listar_un_ticket(id):
    """
    Retorna un solo ticket por su ID (JSON).
    """
    ticket = ticket.query.get_or_404(id)

    data = {
        'id': ticket.id,
        'titulo': ticket.titulo,
        'descripcion': ticket.descripcion,
        'profesor_id': ticket.profesor_id
    }

    return jsonify(data), 200


@main.route('/tickets', methods=['POST'])
def crear_ticket():
    """
    Crea un ticket sin validación.
    Espera JSON con 'titulo', 'descripcion' y 'tecnico_id'.
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    ticket = ticket(
        titulo=data.get('titulo'),
        descripcion=data.get('descripcion'),
        tecnico_id=data.get('tecnico_id')  # sin validación de usuario
    )

    db.session.add(ticket)
    db.session.commit()

    return jsonify({'message': 'Ticket creado', 'id': ticket.id, 'tecnico_id': ticket.tecnico_id}), 201

@main.route('/tickets/<int:id>', methods=['PUT'])
def actualizar_ticket(id):
    """
    Actualiza un ticket sin validación de usuario o permisos.
    """
    ticket = ticket.query.get_or_404(id)
    data = request.get_json()

    ticket.titulo = data.get('titulo', ticket.titulo)
    ticket.descripcion = data.get('descripcion', ticket.descripcion)
    ticket.tecnico_id = data.get('tecnico_id', ticket.tecnico_id)

    db.session.commit()

    return jsonify({'message': 'Ticket actualizado', 'id': ticket.id}), 200

@main.route('/tickets/<int:id>', methods=['DELETE'])
def eliminar_ticket(id):
    """
    Elimina un ticket sin validación de permisos.
    """
    ticket = ticket.query.get_or_404(id)
    db.session.delete(ticket)
    db.session.commit()

    return jsonify({'message': 'Ticket eliminado', 'id': ticket.id}), 200
