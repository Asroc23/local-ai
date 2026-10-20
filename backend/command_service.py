# ==========================================
# COMMAND SERVICE
# ==========================================


class CommandService:

    def __init__(
        self,
        conversation,
        memory_service,
        system_message
    ):

        self.conversation = conversation
        self.memory_service = memory_service
        self.system_message = system_message

    # ==========================================
    # GENERAR TÍTULO
    # ==========================================

    def generar_titulo(
        self,
        prompt,
        max_length=40
    ):

        titulo = " ".join(
            prompt.split()
        )

        if len(titulo) > max_length:

            titulo = (
                titulo[:max_length].rstrip()
                + "..."
            )

        return titulo

    # ==========================================
    # MOSTRAR CONVERSACIONES
    # ==========================================

    def mostrar_conversaciones(self):

        conversaciones = (
            self.conversation.listar()
        )

        if not conversaciones:

            print(
                "\n📭 No hay conversaciones.\n"
            )

            return

        print(
            "\n==================================="
        )

        print(
            "          CONVERSACIONES"
        )

        print(
            "==================================="
        )

        for conversation in conversaciones:

            conversation_id = conversation[0]
            title = conversation[1]
            created_at = conversation[2]

            print(
                f"[{conversation_id}] "
                f"{title} "
                f"({created_at})"
            )

        print(
            "===================================\n"
        )

    # ==========================================
    # MOSTRAR MEMORIAS
    # ==========================================

    def mostrar_memorias(self):

        memorias = (
            self.memory_service.buscar_memorias()
        )

        if not memorias:

            print(
                "\n🧠 No hay memorias guardadas."
            )

            return

        print(
            "\n" + "=" * 50
        )

        print(
            "🧠 MEMORIAS PERMANENTES"
        )

        print(
            "=" * 50
        )

        for memoria in memorias:

            print(
                f"\n[{memoria[0]}] "
                f"{memoria[1]}"
            )

            print(
                f"   Clave: {memoria[2]}"
            )

            print(
                f"   Valor: {memoria[3]}"
            )

            print(
                f"   Importancia: {memoria[4]}"
            )

            print(
                f"   Creada: {memoria[5]}"
            )

            print(
                f"   Actualizada: {memoria[6]}"
            )

    # ==========================================
    # MOSTRAR UNA MEMORIA
    # ==========================================

    def mostrar_memoria(
        self,
        memory_id
    ):

        memoria = (
            self.memory_service.obtener_memoria(
                memory_id
            )
        )

        if not memoria:

            print(
                f"\n❌ No existe la memoria "
                f"con ID {memory_id}."
            )

            return

        print(
            "\n" + "=" * 50
        )

        print(
            "🧠 MEMORIA"
        )

        print(
            "=" * 50
        )

        print(
            f"\nID: {memoria[0]}"
        )

        print(
            f"Categoría: {memoria[1]}"
        )

        print(
            f"Clave: {memoria[2]}"
        )

        print(
            f"Valor: {memoria[3]}"
        )

        print(
            f"Importancia: {memoria[4]}"
        )

        print(
            f"Creada: {memoria[5]}"
        )

        print(
            f"Actualizada: {memoria[6]}"
        )

    # ==========================================
    # CREAR CONVERSACIÓN
    # ==========================================

    def crear_conversacion(self):

        return self.conversation.crear()

    # ==========================================
    # OBTENER CONVERSACIÓN
    # ==========================================

    def obtener_conversacion(
        self,
        conversation_id
    ):

        return self.conversation.obtener(
            conversation_id
        )

    # ==========================================
    # ABRIR CONVERSACIÓN
    # ==========================================

    def abrir_conversacion(
        self,
        conversation_id
    ):

        conversation_data = (
            self.conversation.obtener(
                conversation_id
            )
        )

        if not conversation_data:

            return None

        messages = (
            self.memory_service.cargar_memoria(
                conversation_id
            )
        )

        mensajes_reales = (
            self.memory_service.contar_mensajes_reales(
                messages
            )
        )

        return {
            "conversation_id": conversation_id,
            "messages": messages,
            "mensajes_reales": mensajes_reales
        }

    # ==========================================
    # BORRAR CONVERSACIÓN
    # ==========================================

    def borrar_conversacion(
        self,
        conversation_id
    ):

        conversation_data = (
            self.conversation.obtener(
                conversation_id
            )
        )

        if not conversation_data:

            return False

        self.conversation.eliminar(
            conversation_id
        )

        return True

    # ==========================================
    # CAMBIAR TÍTULO
    # ==========================================

    def cambiar_titulo(
        self,
        conversation_id,
        titulo
    ):

        self.conversation.cambiar_titulo(
            conversation_id,
            titulo
        )

    # ==========================================
    # EDITAR MEMORIA PERMANENTE
    # ==========================================

    def editar_memoria(
        self,
        memory_id,
        categoria,
        clave,
        valor,
        importancia
    ):

        memoria = (
            self.memory_service.obtener_memoria(
                memory_id
            )
        )

        if not memoria:

            return False

        self.memory_service.actualizar_memoria(
            memory_id,
            categoria,
            clave,
            valor,
            importancia
        )

        return True

    # ==========================================
    # ELIMINAR MEMORIA PERMANENTE
    # ==========================================

    def eliminar_memoria(
        self,
        memory_id
    ):

        memoria = (
            self.memory_service.obtener_memoria(
                memory_id
            )
        )

        if not memoria:

            return False

        self.memory_service.eliminar_memoria(
            memory_id
        )

        return True

    # ==========================================
    # LIMPIAR MEMORIA RAM
    # ==========================================

    def limpiar_memoria(self):

        return [
            self.system_message.copy()
        ]