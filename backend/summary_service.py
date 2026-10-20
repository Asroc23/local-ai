# ==========================================
# SUMMARY SERVICE
# ==========================================


class SummaryService:

    def __init__(
        self,
        memory
    ):

        self.memory = memory

    # ==========================================
    # OBTENER ÚLTIMO RESUMEN
    # ==========================================

    def obtener_ultimo_resumen(
        self,
        conversation_id
    ):

        return self.memory.db.get_summary_message_count(
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