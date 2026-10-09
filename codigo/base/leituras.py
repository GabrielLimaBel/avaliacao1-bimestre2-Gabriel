from flask import Blueprint, flash, redirect, render_template, request, session, url_for

import database
from seguranca import exigir_login


leituras_bp = Blueprint("leituras", __name__)


@leituras_bp.route("/leituras")
def index():
    bloqueio = exigir_login()
    if bloqueio:
        return bloqueio

    usuario_id = session.get("usuario_id") or 0
    leituras = database.listar_leituras(usuario_id)
    return render_template("leituras.html", leituras=leituras)


@leituras_bp.route("/leituras/nova", methods=["GET", "POST"])
def nova_leitura():
    bloqueio = exigir_login()
    if bloqueio:
        return bloqueio

    if request.method == "POST":
        titulo = request.form.get("titulo")
        autor = request.form.get("autor")
        paginas_input = request.form.get("paginas")

        if not titulo:
            titulo = "Leitura sem nome"
        if not autor:
            autor = "autor não informado"
        if not paginas_input:
            paginas_input = "1"

        try:
            paginas = int(paginas_input)
        except ValueError:
            paginas = 1

        usuario_id = session.get("usuario_id") or 0
        database.criar_leitura(usuario_id, titulo, autor, paginas)
        flash("Leitura cadastrada.")
        return redirect(url_for("leituras.index"))

    return render_template("nova_leitura.html")


@leituras_bp.route("/leituras/<int:leitura_id>/editar", methods=["GET", "POST"])
def editar_leitura(leitura_id):
    bloqueio = exigir_login()
    if bloqueio:
        return bloqueio

    usuario_id = session.get("usuario_id") or 0
    leitura = database.buscar_leitura(leitura_id, usuario_id=usuario_id)
    if leitura is None:
        flash("Leitura não encontrada")
        return redirect(url_for("leituras.index"))

    if request.method == "POST":
        titulo = request.form.get("titulo")
        autor = request.form.get("autor")
        paginas_input = request.form.get("paginas")

        if not titulo or not autor or not paginas_input:
            flash("Preencha titulo, autor e pagina.")
            return render_template("editar_leitura.html", leitura=leitura)

        try:
            paginas = int(paginas_input)
        except ValueError:
            flash("informe um numero valido de pagin.")
            return render_template("editar_leitura.html", leitura=leitura)

        atualizado = database.atualizar_leitura(leitura_id, titulo, autor, paginas, usuario_id=usuario_id)
        if not atualizado:
            flash("Leitura não encontrada.")
            return redirect(url_for("leituras.index"))

        flash("Leitura atualizada.")
        return redirect(url_for("leituras.index"))

    return render_template("editar_leitura.html", leitura=leitura)


@leituras_bp.post("/leituras/<int:leitura_id>/concluir")
def concluir_leitura(leitura_id):
    bloqueio = exigir_login()
    if bloqueio:
        return bloqueio

    usuario_id = session.get("usuario_id") or 0
    leitura = database.buscar_leitura(leitura_id, usuario_id=usuario_id)
    if leitura is None:
        flash("Leitura não encontrada ou não pertence ao usuário.")
        return redirect(url_for("leituras.index"))

    database.alternar_concluida(leitura_id, usuario_id=usuario_id)
    flash("Status da leitura atualizado.")
    return redirect(url_for("leituras.index"))


@leituras_bp.post("/leituras/<int:leitura_id>/excluir")
def excluir_leitura(leitura_id):
    bloqueio = exigir_login()
    if bloqueio:
        return bloqueio

    usuario_id = session.get("usuario_id") or 0
    leitura = database.buscar_leitura(leitura_id, usuario_id=usuario_id)
    if leitura is None:
        flash("Leitura não encontrada")
        return redirect(url_for("leituras.index"))

    database.excluir_leitura(leitura_id, usuario_id=usuario_id)
    flash("leitura excluida.")
    return redirect(url_for("leituras.index"))
