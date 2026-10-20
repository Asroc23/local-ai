# ==========================================
# EXTRACTOR DE MEMORIA AUTOMÁTICA
# ==========================================


import json


class MemoryExtractor:

    def __init__(
        self,
        client
    ):

        self.client = client

    # ==========================================
    # ANALIZAR MENSAJE
    # ==========================================

    async def analizar(
        self,
        mensaje
    ):

        prompt = f"""
        Analiza el siguiente mensaje de un usuario.

        Determina si contiene información personal,
        preferencias, proyectos, configuraciones,
        objetivos o cualquier otro dato que pueda
        ser útil recordar permanentemente en futuras
        conversaciones.

        NO guardes información temporal, preguntas
        simples, saludos, respuestas casuales ni
        información que solo sea relevante para esta
        conversación.

        Responde ÚNICAMENTE con JSON válido.

        Si NO hay información útil para memoria:

        {{
            "guardar": false
        }}

        Si SÍ hay información útil:

        {{
            "guardar": true,
            "category": "categoría_permitida",
            "key": "clave_descriptiva",
            "value": "información resumida en tercera persona",
            "importance": 1
        }}

        La categoría DEBE ser una de estas opciones:

        - "preferencias" → gustos, preferencias o elecciones del usuario.
        - "proyectos" → proyectos, aplicaciones, trabajos o desarrollos.
        - "configuracion" → modelos, herramientas, configuraciones o tecnologías que utiliza.
        - "objetivos" → metas o cosas que el usuario quiere lograr.
        - "aprendizaje" → conocimientos o tecnologías que el usuario está aprendiendo.
        - "informacion_personal" → información personal estable que sea útil recordar.

        NO utilices categorías en inglés.
        NO inventes nuevas categorías.
        Utiliza exactamente una de las categorías anteriores.

        La importancia debe ser un número entre 1 y 5.

        La respuesta debe estar completamente en español,
        excepto nombres propios, nombres de proyectos,
        lenguajes de programación, tecnologías o herramientas.

        Mensaje del usuario:

        {mensaje}
        """

        respuesta = ""

        async for fragmento in self.client.chat_stream(
            [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        ):

            respuesta += fragmento

        return self._procesar_respuesta(
            respuesta
        )

    # ==========================================
    # PROCESAR RESPUESTA
    # ==========================================

    def _procesar_respuesta(
        self,
        respuesta
    ):

        respuesta = respuesta.strip()

        # --------------------------------------
        # Limpiar bloques Markdown
        # --------------------------------------

        if respuesta.startswith(
            "```json"
        ):

            respuesta = respuesta[
                7:
            ]

        elif respuesta.startswith(
            "```"
        ):

            respuesta = respuesta[
                3:
            ]

        if respuesta.endswith(
            "```"
        ):

            respuesta = respuesta[
                :-3
            ]

        respuesta = respuesta.strip()

        # --------------------------------------
        # Convertir JSON
        # --------------------------------------

        try:

            resultado = json.loads(
                respuesta
            )

        except json.JSONDecodeError:

            return {
                "guardar": False
            }

        # --------------------------------------
        # Validar estructura
        # --------------------------------------

        if not isinstance(
            resultado,
            dict
        ):

            return {
                "guardar": False
            }

        guardar = resultado.get(
            "guardar",
            False
        )

        if not guardar:

            return {
                "guardar": False
            }

        category = resultado.get(
            "category"
        )

        key = resultado.get(
            "key"
        )

        value = resultado.get(
            "value"
        )

        importance = resultado.get(
            "importance",
            3
        )

        if not category or not key or not value:

            return {
                "guardar": False
            }

        try:

            importance = int(
                importance
            )

        except (
            ValueError,
            TypeError
        ):

            importance = 3

        if importance < 1:

            importance = 1

        if importance > 5:

            importance = 5

        return {
            "guardar": True,
            "category": str(
                category
            ).strip(),
            "key": str(
                key
            ).strip(),
            "value": str(
                value
            ).strip(),
            "importance": importance
        }