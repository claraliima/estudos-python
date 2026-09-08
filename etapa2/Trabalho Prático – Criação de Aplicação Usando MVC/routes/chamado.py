from flask import Blueprint
#from controllers.usuario_controller import main
usuario_bp = Blueprint("usuario_bp", __name__, url_prefix="api/")

usuario_bp.add_url_route("/usuarios", view_func = busca_usuarios(), methods = ["GET"])
