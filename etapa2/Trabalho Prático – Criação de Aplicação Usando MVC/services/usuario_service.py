from repositories import UsuarioRepository
from database import db

class UsuarioService:
    @staticmethod
    def verificar_qtde_chamados(id):
        chamados = UsuarioRepository.listar_chamados_usuario(id)
        if len(chamados) >= 5:
            raise ValueError("Usuário não pode ter mais de 5 chamados abertos.")
        return True 
    
    @staticmethod
    def permitir_excluir(id):
        if UsuarioRepository.listar_chamados_usuario(id):
            raise ValueError("Usuário não pode ser excluído, existem chamados vinculados a ele.")
        
        else:
            UsuarioRepository.deletar(UsuarioRepository.buscar_por_id(id))