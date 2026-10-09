from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

import database


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        if nome == "":
            nome = "Usuario"

        if email == "" or senha == "":
            flash("Preencha tudo ai")
            return redirect(url_for("auth.registro"))

        email = email.lower()

        ja_existe = database.buscar_usuario_por_email(email)
        if ja_existe is not None:
            flash("email ja cadastrado, tenta outro.")
            return redirect(url_for("auth.registro"))

        senha_hash = generate_password_hash(senha)
        database.criar_usuario(nome, email, senha_hash)
        flash("Cadastro feito. Agora entra.")
        return redirect(url_for("auth.login"))

    return render_template("registro.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        if email == "":
            flash("Qual o email?")
            return redirect(url_for("auth.login"))

        email = email.lower()

        usuario = database.buscar_usuario_por_email(email)
        if usuario is None:
            flash("Credenciais invalidas.")
            return redirect(url_for("auth.login"))

        if not check_password_hash(usuario.senha_hash, senha):
            flash("Senha errada. Tenta de novo.")
            return redirect(url_for("auth.login"))

        session["usuario_id"] = usuario.id
        session["usuario_nome"] = usuario.nome
        flash("Login ok.")
        return redirect(url_for("leituras.index"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("saiu")
    return redirect(url_for("auth.login"))
