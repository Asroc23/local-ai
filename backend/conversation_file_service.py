from pathlib import Path
import shutil
import uuid


class ConversationFileService:

    def __init__(self, directorio_base="data/files"):
        self.directorio_base = Path(directorio_base)

        self.directorio_base.mkdir(
            parents=True,
            exist_ok=True
        )

    # ==========================================
    # OBTENER DIRECTORIO DE CONVERSACIÓN
    # ==========================================

    def obtener_directorio(self, conversation_id):

        return (
            self.directorio_base
            / f"conversation_{conversation_id}"
        )

    # ==========================================
    # CREAR DIRECTORIO DE CONVERSACIÓN
    # ==========================================

    def crear_directorio(self, conversation_id):

        directorio = self.obtener_directorio(
            conversation_id
        )

        directorio.mkdir(
            parents=True,
            exist_ok=True
        )

        return directorio

    # ==========================================
    # GUARDAR ARCHIVO EN CONVERSACIÓN
    # ==========================================

    def guardar_archivo(
        self,
        conversation_id,
        ruta_origen
    ):

        ruta_origen = Path(ruta_origen)

        if not ruta_origen.is_file():
            raise FileNotFoundError(
                f"No se encontró el archivo: {ruta_origen}"
            )

        directorio = self.crear_directorio(
            conversation_id
        )

        nombre = ruta_origen.name
        destino = directorio / nombre

        # Evitar sobrescribir archivos existentes.
        if destino.exists():

            nombre_unico = uuid.uuid4().hex[:8]

            destino = (
                directorio
                / f"{ruta_origen.stem}_{nombre_unico}"
                f"{ruta_origen.suffix}"
            )

        shutil.copy2(
            ruta_origen,
            destino
        )

        return destino

    # ==========================================
    # ELIMINAR ARCHIVOS DE CONVERSACIÓN
    # ==========================================

    def eliminar_archivos(self, conversation_id):

        directorio = self.obtener_directorio(
            conversation_id
        )

        if directorio.exists():

            shutil.rmtree(directorio)

            return True

        return False