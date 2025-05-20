from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from app.forms import TicketForm, ChangePasswordForm
from app.models import db, Ticket, User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/cambiar-password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('Current password is incorrect.')
            return render_template('cambiar_password.html', form=form)
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('✅ Password updated successfully.')
        return redirect(url_for('main.dashboard'))
    return render_template('cambiar_password.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.role.name == 'Usuario':
        tickets = Ticket.query.all()
    else:
        tickets = Ticket.query.filter_by(tecnico_id=current_user.id).all()
    return render_template('dashboard.html', tickets=tickets)

@main.route('/tickets', methods=['GET', 'POST'])
@login_required
def tickets():
    form = TicketForm()
    # Asignar choices para tecnico_id
    tecnicos = User.query.join(User.role).filter_by(name='Técnico').all()
    form.tecnico_id.choices = [(t.id, t.username) for t in tecnicos]

    if request.method == 'POST':
        if request.is_json:
            # Si es JSON (API)
            data = request.get_json()
            asunto = data.get('asunto')
            descripcion = data.get('descripcion')
            prioridad = data.get('prioridad')
            tecnico_id = data.get('tecnico_id')
            # Validación básica
            if not asunto or not descripcion or not prioridad:
                return jsonify({"error": "Faltan datos requeridos"}), 400
            ticket = Ticket(
                asunto=asunto,
                descripcion=descripcion,
                prioridad=prioridad,
                usuario_id=current_user.id,
                tecnico_id=tecnico_id,
                estado='Abierto'
            )
            db.session.add(ticket)
            db.session.commit()
            return jsonify({"message": "Ticket creado exitosamente"}), 201
        else:
            # Si es formulario HTML
            if form.validate_on_submit():
                ticket = Ticket(
                    asunto=form.asunto.data,
                    descripcion=form.descripcion.data,
                    usuario_id=current_user.id,
                    tecnico_id=form.tecnico_id.data if form.tecnico_id.data else None,
                    prioridad=form.prioridad.data,
                    estado='Abierto'
                )
                db.session.add(ticket)
                db.session.commit()
                flash("Ticket created successfully.")
                return redirect(url_for('main.dashboard'))

    return render_template('ticket_form.html', form=form)

@main.route('/tickets/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_ticket(id):
    ticket = Ticket.query.get_or_404(id)
    if current_user.role.name not in ['Admin', 'Tecnico'] or (
        ticket.tecnico_id != current_user.id and current_user.role.name != 'Admin'):
        flash('You do not have permission to edit this ticket.')
        return redirect(url_for('main.dashboard'))

    form = TicketForm(obj=ticket)
    # Asignar choices para tecnico_id también aquí
    tecnicos = User.query.join(User.role).filter_by(name='Técnico').all()
    form.tecnico_id.choices = [(t.id, t.username) for t in tecnicos]

    if form.validate_on_submit():
        ticket.asunto = form.asunto.data
        ticket.descripcion = form.descripcion.data
        ticket.prioridad = form.prioridad.data
        ticket.estado = form.estado.data
        ticket.tecnico_id = form.tecnico_id.data
        db.session.commit()
        flash("Ticket updated successfully.")
        return redirect(url_for('main.dashboard'))

    return render_template('ticket_form.html', form=form, editar=True)

@main.route('/tickets/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_ticket(id):
    ticket = Ticket.query.get_or_404(id)
    if current_user.role.name not in ['Admin', 'Tecnico'] or (
        ticket.tecnico_id != current_user.id and current_user.role.name != 'Admin'):
        flash('You do not have permission to delete this ticket.')
        return redirect(url_for('main.dashboard'))
    db.session.delete(ticket)
    db.session.commit()
    flash("Ticket deleted successfully.")
    return redirect(url_for('main.dashboard'))

@main.route('/usuarios')
@login_required
def listar_usuarios():
    if current_user.role.name != 'Admin':
        flash("You do not have permission to view this page.")
        return redirect(url_for('main.dashboard'))
    usuarios = User.query.join(User.role).all()
    return render_template('usuarios.html', usuarios=usuarios)

