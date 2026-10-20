from backend.database import Database, DatabaseError


class ConversationService:
    """
    Servicio encargado de gestionar la lógica
    relacionada con las conversaciones.
    """

    DEFAULT_TITLE = "Nueva conversación"

    def __init__(self, db: Database):
        self.db = db

    # ==========================================
    # CREAR CONVERSACIÓN
    # ==========================================

    def crear(self, title=None):

        if title is None or not title.strip():
            title = self.DEFAULT_TITLE

        return self.db.create_conversation(
            title.strip()
        )

    # ==========================================
    # LISTAR CONVERSACIONES
    # ==========================================

    def listar(self):

        return self.db.get_conversations()

    # ==========================================
    # OBTENER CONVERSACIÓN
    # ==========================================

    def obtener(self, conversation_id):

        return self.db.get_conversation(
            conversation_id
        )

    # ==========================================
    # EXISTE CONVERSACIÓN
    # ==========================================

    def existe(self, conversation_id):

        conversation = self.obtener(
            conversation_id
        )

        return conversation is not None

    # ==========================================
    # CAMBIAR TÍTULO
    # ==========================================

    def cambiar_titulo(
        self,
        conversation_id,
        title
    ):

        if not title or not title.strip():

            raise DatabaseError(
                "El título no puede estar vacío."
            )

        self.db.update_conversation_title(
            conversation_id,
            title.strip()
        )

    # ==========================================
    # GUARDAR MENSAJE
    # ==========================================

    def guardar_mensaje(
        self,
        conversation_id,
        role,
        content
    ):

        if not content or not content.strip():

            raise DatabaseError(
                "El contenido del mensaje no puede estar vacío."
            )

        self.db.save_message(
            conversation_id,
            role,
            content
        )

    # ==========================================
    # OBTENER MENSAJES
    # ==========================================

    def obtener_mensajes(
        self,
        conversation_id
    ):

        return self.db.get_messages(
            conversation_id
        )

    # ==========================================
    # ELIMINAR CONVERSACIÓN
    # ==========================================

    def eliminar(self, conversation_id):

        if not self.existe(conversation_id):

            raise DatabaseError(
                "La conversación no existe."
            )

        self.db.delete_conversation(
            conversation_id
        )