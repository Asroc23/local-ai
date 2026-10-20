# ==========================================
# SERVICIO DE ARCHIVOS
# ==========================================

from pypdf import PdfReader


class FileService:

    def leer_pdf(self, ruta):

        lector = PdfReader(ruta)

        texto = []

        for pagina in lector.pages:

            contenido = pagina.extract_text()

            if contenido:
                texto.append(contenido)

        return "\n\n".join(texto)