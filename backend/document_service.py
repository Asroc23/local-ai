
# ==========================================
# SERVICIO DE DOCUMENTOS
# ==========================================


class DocumentService:

    def __init__(self):

        # Documentos disponibles en la conversación actual.
        self.documentos = []

    # ==========================================
    # GUARDAR DOCUMENTO
    # ==========================================

    def guardar(
        self,
        nombre,
        texto,
        ruta
    ):

        # Evitar registrar dos veces la misma ruta.
        for documento in self.documentos:

            if documento["ruta"] == ruta:

                documento["nombre"] = nombre
                documento["texto"] = texto

                return

        self.documentos.append({
            "nombre": nombre,
            "texto": texto,
            "ruta": ruta
        })

    # ==========================================
    # COMPROBAR SI HAY DOCUMENTOS
    # ==========================================

    def tiene_documento(self):

        return bool(self.documentos)

    # ==========================================
    # OBTENER DOCUMENTOS
    # ==========================================

    def obtener(self):

        # Mantener compatibilidad con código que espera
        # un solo documento.
        if len(self.documentos) == 1:
            return self.documentos[0].copy()

        # Devolver una lista cuando hay varios.
        return [
            documento.copy()
            for documento in self.documentos
        ]

    # ==========================================
    # OBTENER CONTEXTO
    # ==========================================

    def obtener_contexto(
        self,
        limite=None
    ):

        if not self.documentos:
            return ""

        partes = []
        caracteres_usados = 0

        for documento in self.documentos:

            nombre = documento["nombre"]
            texto = documento["texto"]

            encabezado = (
                f"\n\n=== DOCUMENTO: {nombre} ===\n\n"
            )

            # Respetar el límite combinado de caracteres.
            if limite is not None:

                disponibles = (
                    limite - caracteres_usados
                    - len(encabezado)
                )

                if disponibles <= 0:
                    break

                texto = texto[:disponibles]

            parte = encabezado + texto

            partes.append(parte)
            caracteres_usados += len(parte)

            if (
                limite is not None
                and caracteres_usados >= limite
            ):
                break

        return "".join(partes).strip()

    # ==========================================
    # PREPARAR CONTEXTO DE LOS DOCUMENTOS
    # ==========================================

    def preparar_contexto(self, limite=12000):

        if not self.documentos:
            return ""

        contexto = self.obtener_contexto(limite)

        if not contexto:
            return ""

        return (
            "DOCUMENTOS ADJUNTOS A ESTA CONVERSACIÓN:\n"
            "Cada sección identifica el archivo del que "
            "procede su contenido.\n"
            "Utiliza los documentos pertinentes para "
            "responder y distingue sus fuentes.\n\n"
            + contexto
        )

    # ==========================================
    # LIMPIAR DOCUMENTOS
    # ==========================================

    def limpiar(self):

        self.documentos.clear()
