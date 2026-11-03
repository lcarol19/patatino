"""
AnimalController — rotas relacionadas a animais.
Só chama services; zero SQL aqui.
"""
from flask import (Blueprint, render_template, request,
    redirect, url_for, flash, abort, session, current_app)

import secrets

from services.animal_service import AnimalService

animal_bp = Blueprint("animal", __name__)
service  = AnimalService()

def admin_obrigatorio():
    if not session.get("admin_autorizado"):
        flash("Faça a autenticação para acessar essa área.", "warning")
        return redirect(url_for("animal.admin_acesso"))
    return None

@animal_bp.route("/admin/acesso", methods=["GET", "POST"])
def admin_acesso():
    if session.get("admin_autorizado"):
        return redirect(url_for("animal.home"))
    if request.method == "POST":
        senha_digitada = request.form.get("senha", "")
        senha_correta = current_app.config.get("SENHA_ADMIN")

        if senha_correta and secrets.compare_digest(
            senha_digitada, senha_correta
        ):
            session.clear()
            session["admin_autorizado"] = True
            session.permanent = True
            flash("Acesso administrativo autorizado! 🐾", "success")
            return redirect(url_for("animal.home"))

        flash("Senha incorreta. Tente novamente.", "danger")

    return render_template("admin_login.html")

@animal_bp.route("/admin/sair")
def admin_sair():
    session.clear()
    flash("Você saiu da área administrativa.", "info")
    return redirect(url_for("animal.home"))

@animal_bp.route("/")
def home():
    """Catálogo público de animais disponíveis para adoção."""
    especie = request.args.get("especie", "")
    porte   = request.args.get("porte", "")
    sexo    = request.args.get("sexo", "")
    busca   = request.args.get("q", "").strip()
    page    = request.args.get("page", 1, type=int)

    animais, total, total_paginas = service.listar_catalogo(
        especie=especie, porte=porte, sexo=sexo,
        busca=busca, page=page,
    )

    return render_template(
        "home.html",
        animais=animais, total=total,
        page=page, total_paginas=total_paginas,
        especie=especie, porte=porte,
        sexo=sexo, busca=busca,
    )

@animal_bp.route("/animal/<int:id_animal>")
def detalhe(id_animal: int):
    """Detalhe do animal com carrossel de fotos."""
    animal = service.buscar_por_id(id_animal)
    if not animal:
        abort(404)
    return render_template("animal.html", animal=animal)

@animal_bp.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    """Formulário de acolhimento — cadastro de novo animal."""
    acesso = admin_obrigatorio()
    if acesso:
        return acesso
    if request.method == "POST":
        try:
            arquivos  = request.files.getlist("fotos_animal")
            id_animal = service.cadastrar(request.form, arquivos)
            flash("Animal cadastrado com sucesso! 🐾", "success")
            return redirect(url_for("animal.detalhe", id_animal=id_animal))
        except ValueError as e:
            flash(str(e), "warning")
        except Exception as e:
            import traceback
            traceback.print_exc()
            flash(f"Erro inesperado: {e}", "danger")

    return render_template("cadastrar_animal.html")


@animal_bp.route("/editar/<int:id_animal>", methods=["GET", "POST"])
def editar(id_animal: int):
    """Edição de animal cadastrado."""
    acesso = admin_obrigatorio()
    if acesso:
        return acesso
    if request.method == "POST":
        try:
            arquivos     = request.files.getlist("fotos_animal")
            fotos_remover = request.form.getlist("fotos_remover")
            service.atualizar(id_animal, request.form, arquivos, fotos_remover)
            flash("Animal atualizado com sucesso! 🐾", "success")
            return redirect(url_for("animal.detalhe", id_animal=id_animal))
        except ValueError as e:
            flash(str(e), "warning")
        except Exception as e:
            flash(f"Erro inesperado: {e}", "danger")

    animal = service.buscar_por_id(id_animal)
    if not animal:
        abort(404)
    return render_template("editar_animal.html", animal=animal)


@animal_bp.route("/excluir/<int:id_animal>", methods=["POST"])
def excluir(id_animal: int):
    """Remove animal e suas fotos do Cloudinary."""
    acesso = admin_obrigatorio()
    if acesso:
        return acesso
    try:
        service.excluir(id_animal)
        flash("Animal removido.", "info")
    except Exception as e:
        flash(f"Erro ao excluir: {e}", "danger")
    return redirect(url_for("animal.home"))
