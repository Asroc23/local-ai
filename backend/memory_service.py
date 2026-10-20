# ==========================================
# MEMORY SERVICE
# ==========================================


class MemoryService:

    def __init__(
        self,
        memory
    ):

        self.memory = memory

    # ==========================================
    # CONTAR MENSAJES REALES
    # ==========================================

    def contar_mensajes_reales(
        self,
        messages
    ):

        return self.memory.contar_mensajes_reales(
            messages
        )

    # ==========================================
    # CARGAR MEMORIA
    # ==========================================

    def cargar_memoria(
        self,
        conversation_id,
        max_messages=20
    ):

        return self.memory.cargar_memoria(
            conversation_id,
            max_messages
        )

    # ==========================================
    # LIMITAR MEMORIA
    # ==========================================

    def limitar_memoria(
        self,
        messages,
        max_messages=20
    ):

        return self.memory.limitar_memoria(
            messages,
            max_messages
        )

    # ==========================================
    # CONTAR MENSAJES DE LA CONVERSACIÓN
    # ==========================================

    def contar_mensajes_conversacion(
        self,
        conversation_id
    ):

        return self.memory.contar_mensajes_conversacion(
            conversation_id
        )

    # ==========================================
    # GENERAR RESUMEN
    # ==========================================

    async def generar_resumen(
        self,
        conversation_id,
        messages
    ):

        return await self.memory.generar_resumen(
            conversation_id,
            messages
        )

    # ==========================================
    # GUARDAR MEMORIA
    # ==========================================

    def guardar_memoria(
        self,
        category,
        key,
        value,
        importance=3
    ):

        return self.memory.guardar_memoria(
            category,
            key,
            value,
            importance
        )

    # ==========================================
    # GUARDAR MEMORIA AUTOMÁTICA
    # ==========================================

    def guardar_memoria_automatica(
        self,
        resultado
    ):

        return self.memory.guardar_memoria_automatica(
            resultado
        )

    # ==========================================
    # BUSCAR TODAS LAS MEMORIAS
    # ==========================================

    def buscar_memorias(
        self
    ):

        return self.memory.buscar_memorias()

    # ==========================================
    # OBTENER UNA MEMORIA
    # ==========================================

    def obtener_memoria(
        self,
        memory_id
    ):

        return self.memory.obtener_memoria(
            memory_id
        )

    # ==========================================
    # ACTUALIZAR MEMORIA
    # ==========================================

    def actualizar_memoria(
        self,
        memory_id,
        category,
        key,
        value,
        importance
    ):

        return self.memory.actualizar_memoria(
            memory_id,
            category,
            key,
            value,
            importance
        )

    # ==========================================
    # ELIMINAR MEMORIA
    # ==========================================

    def eliminar_memoria(
        self,
        memory_id
    ):

        return self.memory.eliminar_memoria(
            memory_id
        )

    # ==========================================
    # BUSCAR MEMORIAS RELEVANTES
    # ==========================================

    def buscar_memorias_relevantes(
        self,
        texto,
        limite=5
    ):

        return self.memory.buscar_memorias_relevantes(
            texto,
            limite
        )

    # ==========================================
    # OBTENER CONTEXTO DE MEMORIA
    # ==========================================

    def obtener_contexto_memoria(
        self,
        texto,
        limite=5
    ):

        return self.memory.obtener_contexto_memoria(
            texto,
            limite
        )