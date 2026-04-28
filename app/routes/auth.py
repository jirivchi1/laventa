from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

from app.models.usuario import Usuario

auth_bp = Blueprint('auth', __name__)


def _redirect_por_rol(usuario):
    """Redirige al panel correspondiente según el rol del usuario."""
    if usuario.es_admin:
        return redirect(url_for('admin.dashboard'))
    elif usuario.es_limpieza:
        return redirect(url_for('limpieza.dashboard'))
    return redirect(url_for('main.inicio'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return _redirect_por_rol(current_user)

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.check_password(password):
            login_user(usuario)
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return _redirect_por_rol(usuario)

        flash('Email o contraseña incorrectos.', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada.', 'info')
    return redirect(url_for('main.inicio'))
