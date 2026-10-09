from flask import flash, redirect, session, url_for


def exigir_login():
    usuario_id = session.get("usuario_id", 0)
    if not usuario_id:
        flash("voce precisa logar antes.")
        return redirect(url_for("auth.login"))
    return None
