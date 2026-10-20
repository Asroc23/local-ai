# ==========================================
# MEMORIA
# ==========================================


class Memory:

    def __init__(
        self,
        db,
        system_message,
        client
    ):

        self.db = db
        self.system_message = system_message
        self.client = client

    # ==========================================
    # CONTAR MENSAJES REALES
    # ==========================================

    def contar_mensajes_reales(
        self,
        messages
    ):

        return sum(
            1
            for message in messages
            if message["role"] in (
                "user",
                "assistant"
            )
        )

    # ==========================================
    # CARGAR MEMORIA
    # ==========================================

    def cargar_memoria(
        self,
        conversation_id,
        max_messages=20
    ):

        mensajes_db = self.db.get_messages(
            conversation_id
        )

        resumen = self.db.get_summary(
            conversation_id
        )

        # ==========================================
        # CREAR SYSTEM
        # ==========================================

        system_content = self.system_message["content"]

        # ==========================================
        # AGREGAR RESUMEN AL SYSTEM
        # ==========================================

        if resumen:

            system_content += (
                "\n\n"
                "Resumen de la conversación anterior:\n\n"
                + resumen
            )

        messages = [
            {
                "role": "system",
                "content": system_content
            }
        ]

        # ==========================================
        # OBTENER MENSAJES REALES
        # ==========================================

        historial = []

        for role, content in mensajes_db:

            if role in (
                "user",
                "assistant"
            ):

                historial.append({
                    "role": role,
                    "content": content
                })

        # ==========================================
        # ASEGURAR PARES VÁLIDOS
        # ==========================================

        if (
            historial
            and historial[0]["role"] == "assistant"
        ):

            historial = historial[1:]

        # ==========================================
        # LIMITAR HISTORIAL
        # ==========================================

        if len(historial) > max_messages:

            historial = historial[-max_messages:]

            if (
                historial
                and historial[0]["role"] == "assistant"
            ):

                historial = historial[1:]

        # ==========================================
        # VALIDAR ALTERNANCIA
        # ==========================================

        historial_valido = []

        ultimo_role = None

        for message in historial:

            role = message["role"]

            # El primer mensaje debe ser user.

            if not historial_valido:

                if role != "user":

                    continue

            # Evitar dos roles iguales consecutivos.

            if ultimo_role == role:

                continue

            historial_valido.append(
                message
            )

            ultimo_role = role

        messages.extend(
            historial_valido
        )

        return messages

    # ==========================================
    # LIMITAR MEMORIA
    # ==========================================

    def limitar_memoria(
        self,
        messages,
        max_messages=20
    ):

        # ==========================================
        # CONSERVAR SYSTEM
        # ==========================================

        system_message = messages[0]

        # ==========================================
        # OBTENER HISTORIAL REAL
        # ==========================================

        historial = []

        for message in messages[1:]:

            if message["role"] in (
                "user",
                "assistant"
            ):

                historial.append(
                    message
                )

        # ==========================================
        # LIMITAR HISTORIAL
        # ==========================================

        if len(historial) > max_messages:

            historial = historial[-max_messages:]

        # ==========================================
        # ASEGURAR QUE COMIENCE EN USER
        # ==========================================

        if (
            historial
            and historial[0]["role"] == "assistant"
        ):

            historial = historial[1:]

        # ==========================================
        # VALIDAR ALTERNANCIA
        # ==========================================

        historial_valido = []

        ultimo_role = None

        for message in historial:

            role = message["role"]

            # El historial debe comenzar con user.

            if not historial_valido:

                if role != "user":

                    continue

            # No permitir dos roles iguales.

            if ultimo_role == role:

                continue

            historial_valido.append(
                message
            )

            ultimo_role = role

        return [
            system_message
        ] + historial_valido

    # ==========================================
    # CONTAR MENSAJES DE LA CONVERSACIÓN
    # ==========================================

    def contar_mensajes_conversacion(
        self,
        conversation_id
    ):

        mensajes = self.db.get_messages(
            conversation_id
        )

        return sum(
            1
            for role, content in mensajes
            if role in (
                "user",
                "assistant"
            )
        )

    # ==========================================
    # GENERAR RESUMEN
    # ==========================================

    async def generar_resumen(
        self,
        conversation_id,
        messages
    ):

        resumen_actual = self.db.get_summary(
            conversation_id
        )

        ultimo_resumen = self.db.get_summary_message_count(
            conversation_id
        )

        # ==========================================
        # OBTENER HISTORIAL COMPLETO DESDE SQLITE
        # ==========================================

        mensajes_db = self.db.get_messages(
            conversation_id
        )

        historial = []

        for role, content in mensajes_db:

            if role in (
                "user",
                "assistant"
            ):

                historial.append({
                    "role": role,
                    "content": content
                })

        # ==========================================
        # COMPROBAR SI TOCA ACTUALIZAR EL RESUMEN
        # ==========================================

        mensajes_totales = len(historial)

        mensajes_nuevos = (
            mensajes_totales - ultimo_resumen
        )

        if (
            mensajes_totales < 20
            or mensajes_nuevos < 20
        ):

            return messages

        # ==========================================
        # SEPARAR MENSAJES ANTIGUOS
        # DE LOS ÚLTIMOS 20
        # ==========================================

        mensajes_antiguos = historial[:-20]

        texto = ""

        for mensaje in mensajes_antiguos:

            role = mensaje["role"]
            content = mensaje["content"]

            texto += (
                f"{role}: {content}\n"
            )

        # ==========================================
        # GENERAR NUEVO RESUMEN
        # ==========================================

        prompt_resumen = f"""
            Actualiza el resumen de esta conversación.

            Tu tarea es crear un resumen preciso y confiable
            para que otro asistente pueda continuar la conversación
            posteriormente.

            REGLAS IMPORTANTES:

            1. Utiliza únicamente información que aparezca
            explícitamente en el resumen anterior o en los
            mensajes de la conversación.

            2. NO inventes nombres, proyectos, preferencias,
            conocimientos, decisiones ni ningún otro dato.

            3. Si una información aparece varias veces,
            considera el contexto y el orden cronológico
            de los mensajes.

            4. Si el usuario corrige una información anterior,
            la corrección más reciente reemplaza a la
            información anterior.

            5. Nunca conserves como válida una información
            que posteriormente haya sido corregida.

            6. Si existe una contradicción y no queda claro
            cuál es la información correcta, NO inventes
            una solución. Conserva únicamente lo que pueda
            determinarse con seguridad.

            7. Presta especial atención a información que pueda
            ser útil en futuras conversaciones:

            - nombre preferido del usuario
            - proyectos actuales
            - preferencias
            - objetivos
            - conocimientos
            - decisiones tomadas
            - información técnica importante
            - correcciones importantes
            - configuraciones importantes
            - contexto relevante

            8. No incluyas conversaciones irrelevantes,
            saludos, respuestas triviales ni información
            temporal que no sea útil posteriormente.

            9. No describas el proceso de resumen.
            Devuelve directamente el resumen.

            RESUMEN ANTERIOR:
            {resumen_actual}

            HISTORIAL DE LA CONVERSACIÓN:
            {texto}

            Genera ahora el nuevo resumen.

            Devuelve únicamente el resumen.
            """

        nuevo_resumen = await self.client.chat(
            [
                {
                    "role": "system",
                    "content": (
                        "Eres un sistema especializado "
                        "en resumir conversaciones."
                    )
                },
                {
                    "role": "user",
                    "content": prompt_resumen
                }
            ],
            temperature=0.2
        )

        # ==========================================
        # GUARDAR RESUMEN EN SQLITE
        # ==========================================

        self.db.save_summary(
            conversation_id,
            nuevo_resumen
        )

        self.db.save_summary_message_count(
            conversation_id,
            mensajes_totales
        )

        print(
            "\n🧠 Resumen de conversación actualizado."
        )

        # ==========================================
        # RECONSTRUIR CONTEXTO
        # ==========================================

        system_content = (
            self.system_message["content"]
        )

        if nuevo_resumen:

            system_content += (
                "\n\n"
                "Resumen de la conversación anterior:"
                "\n\n"
                + nuevo_resumen
            )

        nuevos_messages = [
            {
                "role": "system",
                "content": system_content
            }
        ]

        # ==========================================
        # CONSERVAR SOLO LOS ÚLTIMOS 20
        # ==========================================

        nuevos_messages.extend(
            historial[-20:]
        )

        return nuevos_messages

    # ==========================================
    # GUARDAR MEMORIA PERMANENTE
    # ==========================================

    def guardar_memoria(
        self,
        category,
        key,
        value,
        importance=3
    ):

        return self.db.save_memory(
            category,
            key,
            value,
            importance
        )

    # ==========================================
    # GUARDAR / ACTUALIZAR MEMORIA AUTOMÁTICA
    # ==========================================

    def guardar_memoria_automatica(
        self,
        resultado
    ):

        # --------------------------------------
        # Verificar si el extractor decidió
        # guardar
        # --------------------------------------

        if not resultado.get(
            "guardar",
            False
        ):

            return None

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

        # --------------------------------------
        # Verificar datos obligatorios
        # --------------------------------------

        if not category or not key or not value:

            return None

        # --------------------------------------
        # Buscar memoria existente
        # --------------------------------------

        memoria_existente = (
            self.db.get_memory_by_key(
                category,
                key
            )
        )

        # --------------------------------------
        # Si no existe → crear
        # --------------------------------------

        if not memoria_existente:

            return self.guardar_memoria(
                category,
                key,
                value,
                importance
            )

        # --------------------------------------
        # Memoria existente
        # --------------------------------------

        memory_id = memoria_existente[0]

        valor_existente = memoria_existente[3]

        importancia_existente = memoria_existente[4]

        # --------------------------------------
        # Si el valor no cambió
        # --------------------------------------

        if valor_existente == value:

            return memory_id

        # --------------------------------------
        # Si cambió → actualizar
        # --------------------------------------

        self.actualizar_memoria(
            memory_id,
            category,
            key,
            value,
            importance
        )

        return memory_id

    # ==========================================
    # BUSCAR TODAS LAS MEMORIAS
    # ==========================================

    def buscar_memorias(self):

        return self.db.get_memories()

    # ==========================================
    # OBTENER UNA MEMORIA
    # ==========================================

    def obtener_memoria(
        self,
        memory_id
    ):

        return self.db.get_memory(
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

        return self.db.update_memory(
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

        return self.db.delete_memory(
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

        # ==========================================
        # OBTENER MEMORIAS
        # ==========================================

        memorias = self.db.get_memories()

        if not memorias:

            return []

        # ==========================================
        # NORMALIZAR TEXTO
        # ==========================================

        texto = texto.strip().lower()

        if not texto:

            return []

        # ==========================================
        # DIVIDIR CONSULTA EN PALABRAS
        # ==========================================

        palabras = texto.split()

        # Palabras que normalmente no aportan
        # información relevante para la búsqueda.

        palabras_ignoradas = {
            "el",
            "la",
            "los",
            "las",
            "un",
            "una",
            "unos",
            "unas",
            "de",
            "del",
            "al",
            "a",
            "en",
            "con",
            "por",
            "para",
            "que",
            "qué",
            "y",
            "o",
            "u",
            "es",
            "soy",
            "mi",
            "mis",
            "me",
            "te",
            "se",
            "yo",
            "tu",
            "tú",
            "su",
            "sus",
            "como",
            "cómo",
            "cuál",
            "cual",
            "cuáles",
            "cuales"
        }

        palabras_busqueda = [
            palabra
            for palabra in palabras
            if palabra not in palabras_ignoradas
            and len(palabra) > 2
        ]

        if not palabras_busqueda:

            return []

        # ==========================================
        # CALCULAR RELEVANCIA
        # ==========================================

        resultados = []

        for memoria in memorias:

            memory_id = memoria[0]
            category = memoria[1]
            key = memoria[2]
            value = memoria[3]
            importance = memoria[4]

            category_text = category.lower()
            key_text = key.lower()
            value_text = value.lower()

            # Todo el contenido de la memoria.

            contenido = (
                f"{category_text} "
                f"{key_text} "
                f"{value_text}"
            )

            puntuacion = 0

            coincidencias = 0

            # ==========================================
            # ANALIZAR CADA PALABRA
            # ==========================================

            for palabra in palabras_busqueda:

                # Coincidencia exacta en la clave.
                if palabra in key_text:

                    puntuacion += 4
                    coincidencias += 1

                # Coincidencia en categoría.
                elif palabra in category_text:

                    puntuacion += 3
                    coincidencias += 1

                # Coincidencia en valor.
                elif palabra in value_text:

                    puntuacion += 2
                    coincidencias += 1

                # Coincidencia general.
                elif palabra in contenido:

                    puntuacion += 1
                    coincidencias += 1

            # ==========================================
            # IMPORTANCIA DE LA MEMORIA
            # ==========================================

            if coincidencias > 0:

                puntuacion += importance

                resultados.append(
                    (
                        puntuacion,
                        memoria
                    )
                )

        # ==========================================
        # ORDENAR POR RELEVANCIA
        # ==========================================

        resultados.sort(
            key=lambda resultado: resultado[0],
            reverse=True
        )

        # ==========================================
        # DEVOLVER SOLO MEMORIAS
        # ==========================================

        return [
            memoria
            for puntuacion, memoria
            in resultados[:limite]
        ]
    # ==========================================
    # CREAR CONTEXTO DE MEMORIA
    # ==========================================

    def obtener_contexto_memoria(
        self,
        texto,
        limite=5
    ):

        memorias = self.buscar_memorias_relevantes(
            texto,
            limite
        )

        if not memorias:

            return ""

        contexto = (
            "Memoria permanente relevante "
            "para esta conversación:\n\n"
        )

        for memoria in memorias:

            memory_id = memoria[0]
            category = memoria[1]
            key = memoria[2]
            value = memoria[3]
            importance = memoria[4]

            contexto += (
                f"- {value}\n"
            )

        return contexto.strip()
