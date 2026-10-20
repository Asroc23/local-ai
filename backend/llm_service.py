# ==========================================
# LLM SERVICE
# ==========================================


class LLMService:

    def __init__(
        self,
        client
    ):

        self.client = client

    # ==========================================
    # STREAMING DE RESPUESTA
    # ==========================================

    async def chat_stream(
        self,
        messages,
        temperature=0.7
    ):

        async for fragmento in self.client.chat_stream(
            messages,
            temperature
        ):

            yield fragmento

    # ==========================================
    # ESTADÍSTICAS DE USO
    # ==========================================

    @property
    def last_usage(self):

        return self.client.last_usage