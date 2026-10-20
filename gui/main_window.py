# ==========================================
# VENTANA PRINCIPAL
# ==========================================

import asyncio

from PySide6.QtCore import (
    QThread,
    Signal,
    Qt,
    QTimer
)

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QLabel,
    QListWidget,
    QMessageBox,
    QInputDialog,
    QScrollArea,
    QDialog,
    QFileDialog,
)

from gui.controller import GUIController
from gui.memory_window import MemoryWindow
from gui.chat_bubble import ChatBubble
from gui.empty_state import EmptyState
from gui.custom_dialog import (
    ConfirmDialog,
    RenameDialog,
)

# ==========================================
# CONFIGURACIÓN
# ==========================================

SYSTEM_MESSAGE = {
    "role": "system",
    "content": (
        "Eres un asistente de inteligencia artificial "
        "útil, claro y preciso. "
        "Mantén el contexto de la conversación."
    )
}


# ==========================================
# WORKER
# ==========================================

class ChatWorker(QThread):

    fragmento = Signal(str)
    terminado = Signal()
    error = Signal(str)

    def __init__(
        self,
        controller,
        prompt
    ):

        super().__init__()

        self.controller = controller
        self.prompt = prompt

    def run(self):

        async def ejecutar():

            try:

                async for texto in (
                    self.controller.enviar_mensaje(
                        self.prompt
                    )
                ):

                    self.fragmento.emit(
                        texto
                    )

                self.terminado.emit()

            except Exception as e:

                self.error.emit(
                    str(e)
                )

        try:

            asyncio.run(
                ejecutar()
            )

        except Exception as e:

            self.error.emit(
                str(e)
            )


# ==========================================
# VENTANA PRINCIPAL
# ==========================================

class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Local AI"
        )

        self.resize(
            1100,
            700
        )

        # ==========================================
        # CONTROLADOR
        # ==========================================

        self.controller = GUIController(
            SYSTEM_MESSAGE
        )

        self.worker = None

        # ==========================================
        # STREAMING SUAVE
        # ==========================================

        self._texto_respuesta = ""
        self._fragmentos_pendientes = []

        self._timer_streaming = QTimer(self)
        self._timer_streaming.setInterval(40)

        self._timer_streaming.timeout.connect(
            self.actualizar_streaming
        )

        # ==========================================
        # INTERFAZ
        # ==========================================

        self.crear_interfaz()

        self.cargar_conversaciones()

        # Seleccionar la conversación activa al iniciar
        self.seleccionar_conversacion_activa()

    # ==========================================
    # CREAR INTERFAZ
    # ==========================================

    def crear_interfaz(self):

        contenedor = QWidget()

        layout_principal = QHBoxLayout()

        layout_principal.setContentsMargins(
            0,
            0,
            0,
            0
        )

        layout_principal.setSpacing(
            0
        )

        # ==========================================
        # PANEL LATERAL
        # ==========================================

        panel_lateral = QVBoxLayout()

        panel_lateral.setContentsMargins(
            12,
            12,
            12,
            12
        )

        panel_lateral.setSpacing(
            10
        )

        titulo = QLabel(
            "🤖 Local AI DoDO"
        )

        titulo.setObjectName(
            "titulo_lateral"
        )

        boton_nueva = QPushButton(
            "🆕 Nueva conversación"
        )

        boton_nueva.setObjectName(
            "boton_nueva"
        )

        boton_memorias = QPushButton(
            "🧠  Memorias"
        )

        boton_memorias.setObjectName("boton_secundario")

        historial = QListWidget()

        historial.setObjectName(
            "historial"
        )

        boton_eliminar = QPushButton("🗑️  Eliminar conversación")
        boton_eliminar.setObjectName("boton_secundario")

        boton_renombrar = QPushButton("✏️  Renombrar conversación")
        boton_renombrar.setObjectName("boton_secundario")

        panel_lateral.addWidget(
            titulo
        )

        panel_lateral.addWidget(
            boton_nueva
        )

        panel_lateral.addWidget(
            boton_memorias
        )

        panel_lateral.addWidget(
            historial
        )

        panel_lateral.addWidget(
            boton_eliminar
        )

        panel_lateral.addWidget(
            boton_renombrar
        )

        panel_lateral_widget = QWidget()

        panel_lateral_widget.setLayout(
            panel_lateral
        )

        panel_lateral_widget.setObjectName(
            "panel_lateral"
        )

        panel_lateral_widget.setStyleSheet(
            """
            #panel_lateral {
                background-color: #f7f7f8;
                border-right: 1px solid #e2e2e2;
            }

            #titulo_lateral {
                color: #222222;
                font-size: 20px;
                font-weight: bold;
                padding: 6px 4px;
                text-align: center;
            }

            #boton_nueva {
                background-color: #2b7cff;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }

            #boton_secundario {
                background-color: #eeeeef;
                color: #333333;
                border: 1px solid #e2e2e3;
                border-radius: 9px;
                padding: 9px 12px;
                text-align: left;
                font-size: 14px;
                font-weight: 500;
                text-align: center;
            }

            #boton_secundario:hover {
                background-color: #e5e5e7;
                border: 1px solid #d8d8da;
            }

            #boton_secundario:pressed {
                background-color: #dcdcdf;
            }

            #boton_nueva:hover {
                background-color: #1f6be0;
            }

            #boton_nueva:pressed {
                background-color: #1859bd;
            }

            #historial {
                background-color: transparent;
                border: none;
                outline: none;
                padding: 4px 0px;
                font-size: 14px;
                color: #333333;
            }

            #historial::item {
                background-color: transparent;
                padding: 10px 12px;
                margin: 3px 0px;
                border-radius: 9px;
                border: 1px solid transparent;
            }

            #historial::item:hover {
                background-color: #eeeeef;
            }

            #historial::item:selected {
                background-color: #dfe9ff;
                color: #1f5fc4;
                border: 1px solid #cbdcff;
                font-weight: 600;
            }

            #historial::item:selected:hover {
                background-color: #dfe9ff;
            }

            """
        )
        # ==========================================
        # PANEL DE CHAT
        # ==========================================

        panel_chat = QVBoxLayout()

        panel_chat.setContentsMargins(
            0,
            0,
            0,
            0
        )

        panel_chat.setSpacing(
            0
        )

        titulo_chat = QLabel(
            "💬  Conversación"
        )

        titulo_chat.setStyleSheet(
            """
            QLabel#titulo_chat {
                background-color: #ffffff;
                color: #222222;
                border-bottom: 1px solid #e2e2e2;
                padding: 14px 18px;
                font-size: 16px;
                font-weight: 600;
            }
            """
        )

        titulo_chat.setObjectName(
            "titulo_chat"
        )

        area_mensajes = QScrollArea()

        area_mensajes.setWidgetResizable(
            True
        )

        area_mensajes.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )

        area_mensajes.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        area_mensajes.setObjectName(
            "area_mensajes"
        )

        contenedor_mensajes = QWidget()

        contenedor_mensajes.setObjectName(
            "contenedor_mensajes"
        )

        layout_mensajes = QVBoxLayout(
            contenedor_mensajes
        )

        layout_mensajes.setContentsMargins(
            10,
            10,
            10,
            10
        )

        layout_mensajes.setSpacing(
            4
        )

        layout_mensajes.addStretch()

        area_mensajes.setWidget(
            contenedor_mensajes
        )

        area_mensajes.setStyleSheet(
            """
            QScrollArea#area_mensajes {
                background-color: #ffffff;
                border: none;
            }

            QWidget#contenedor_mensajes {
                background-color: #ffffff;
            }
            """
        )

        # ==========================================
        # ENTRADA DE MENSAJE
        # ==========================================

        entrada = QLineEdit()

        entrada.setPlaceholderText(
            "Escribe un mensaje..."
        )

        entrada.setFixedHeight(
            46
        )

        entrada.setStyleSheet(
            """
            QLineEdit {
                background-color: #f5f5f5;
                color: #222222;
                border: 1px solid #dddddd;
                border-radius: 20px;
                padding: 0px 16px;
                font-size: 14px;
            }

            QLineEdit:focus {
                border: 1px solid #2b7cff;
            }
            """
        )

        entrada.returnPressed.connect(
            self.enviar_mensaje
        )

        # ==========================================
        # BOTÓN ADJUNTAR ARCHIVO
        # ==========================================

        boton_archivo = QPushButton(
            "📎"
        )

        boton_archivo.setFixedSize(
            46,
            46
        )

        boton_archivo.setToolTip(
            "Adjuntar archivo"
        )

        boton_archivo.setStyleSheet(
            """
            QPushButton {
                background-color: #eeeeef;
                color: #555555;
                border: 1px solid #dddddf;
                border-radius: 23px;
                font-size: 20px;
            }

            QPushButton:hover {
                background-color: #e5e5e7;
            }

            QPushButton:pressed {
                background-color: #dcdcdf;
            }
            """
        )

        # ==========================================
        # BOTÓN ENVIAR
        # ==========================================

        boton_enviar = QPushButton(
            "➤"
        )

        boton_enviar.setFixedSize(
            46,
            46
        )

        boton_enviar.setToolTip(
            "Enviar mensaje"
        )

        boton_enviar.setStyleSheet(
            """
            QPushButton {
                background-color: #2b7cff;
                color: white;
                border: none;
                border-radius: 23px;
                font-size: 20px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #1f6be0;
            }

            QPushButton:pressed {
                background-color: #1859bd;
            }

            QPushButton:disabled {
                background-color: #aaaaaa;
            }
            """
        )

        # ==========================================
        # PANEL DE ENTRADA
        # ==========================================

        panel_entrada = QHBoxLayout()

        panel_entrada.setContentsMargins(
            12,
            10,
            12,
            14
        )

        panel_entrada.setSpacing(
            10
        )

        panel_entrada.addWidget(
            entrada
        )

        panel_entrada.addWidget(
            boton_archivo
        )

        panel_entrada.addWidget(
            boton_enviar
        )

        # ==========================================
        # ARMAR PANEL DE CHAT
        # ==========================================

        panel_chat.addWidget(
            titulo_chat
        )

        panel_chat.addWidget(
            area_mensajes
        )

        panel_chat.setStretch(
            1,
            1
        )

        panel_chat.addLayout(
            panel_entrada
        )

        # ==========================================
        # UNIR PANELES
        # ==========================================

        layout_principal.addWidget(
            panel_lateral_widget,
            1
        )

        layout_principal.addLayout(
            panel_chat,
            3
        )

        contenedor.setLayout(
            layout_principal
        )

        self.setCentralWidget(
            contenedor
        )

        # ==========================================
        # CONECTAR BOTONES
        # ==========================================

        boton_enviar.clicked.connect(
            self.enviar_mensaje
        )

        boton_nueva.clicked.connect(
            self.nueva_conversacion
        )

        historial.itemClicked.connect(
            self.seleccionar_conversacion
        )

        boton_eliminar.clicked.connect(
            self.eliminar_conversacion
        )

        boton_renombrar.clicked.connect(
            self.renombrar_conversacion
        )

        boton_memorias.clicked.connect(
            self.abrir_memorias
        )

        boton_archivo.clicked.connect(
            self.adjuntar_archivo
        )

        # ==========================================
        # GUARDAR REFERENCIAS
        # ==========================================

        self.entrada = entrada

        self.area_mensajes = area_mensajes

        self.contenedor_mensajes = (
            contenedor_mensajes
        )

        self.layout_mensajes = (
            layout_mensajes
        )

        self.boton_enviar = boton_enviar

        self.boton_nueva = boton_nueva

        self.historial = historial

        self.boton_eliminar = (
            boton_eliminar
        )

        self.memory_window = None

        self.boton_archivo = boton_archivo

    # ==========================================
    # ENVIAR MENSAJE
    # ==========================================

    def enviar_mensaje(self):

        if self.controller.conversation_id is None:

            QMessageBox.information(
                self,
                "Sin conversación activa",
                (
                    "No hay una conversación activa.\n\n"
                    "Pulsa «Nueva conversación» "
                    "o selecciona una conversación del historial."
                )
            )

            return

        prompt = (
            self.entrada
            .text()
            .strip()
        )

        if not prompt:

            return

        # ==========================================
        # LIMPIAR ENTRADA
        # ==========================================

        self.entrada.clear()

        # ==========================================
        # MOSTRAR USUARIO
        # ==========================================

        burbuja_usuario = ChatBubble(
            prompt,
            "user"
        )

        self.layout_mensajes.insertWidget(
            self.layout_mensajes.count() - 1,
            burbuja_usuario
        )

        # ==========================================
        # PREPARAR BURBUJA DE LA IA
        # ==========================================

        self.burbuja_ia = ChatBubble(
            "",
            "assistant"
        )

        self._texto_respuesta = ""
        self._fragmentos_pendientes.clear()

        self.layout_mensajes.insertWidget(
            self.layout_mensajes.count() - 1,
            self.burbuja_ia
        )

        # ==========================================
        # DESACTIVAR BOTÓN
        # ==========================================

        self.boton_enviar.setEnabled(
            False
        )

        # ==========================================
        # CREAR WORKER
        # ==========================================

        self.worker = ChatWorker(
            self.controller,
            prompt
        )

        self.worker.fragmento.connect(
            self.mostrar_fragmento
        )

        self.worker.terminado.connect(
            self.generacion_terminada
        )

        self.worker.error.connect(
            self.mostrar_error
        )

        self._timer_streaming.start()
        self.worker.start()

    # ==========================================
    # STREAMING SUAVE
    # ==========================================

    def mostrar_fragmento(self, texto):
        """Recibe fragmentos sin redibujar la interfaz."""

        self._fragmentos_pendientes.append(texto)
        self._texto_respuesta += texto

    def actualizar_streaming(self):
        """Muestra los fragmentos acumulados en un solo lote."""

        if not self._fragmentos_pendientes:
            return

        texto = "".join(
            self._fragmentos_pendientes
        )

        self._fragmentos_pendientes.clear()

        if not texto:
            return

        self.burbuja_ia.mensaje.agregar_texto_streaming(
            texto
        )

        # Desplazar una sola vez por lote, no por fragmento.
        barra = self.area_mensajes.verticalScrollBar()

        barra.setValue(
            barra.maximum()
        )
    # ==========================================
    # GENERACIÓN TERMINADA
    # ==========================================

    def generacion_terminada(self):

        self._timer_streaming.stop()

        # Mostrar cualquier fragmento pendiente.
        self.actualizar_streaming()

        # Aplicar el formato Markdown definitivo una sola vez.
        self.burbuja_ia.actualizar_contenido(
            self._texto_respuesta
        )

        self.cargar_conversaciones()

        self.seleccionar_conversacion_activa()

        if self.memory_window is not None:
            self.memory_window.cargar_memorias()

        self.boton_enviar.setEnabled(True)
        self.entrada.setFocus()

        # Mantener visible el final de la respuesta.
        QTimer.singleShot(
            0,
            lambda: self.area_mensajes.verticalScrollBar().setValue(
                self.area_mensajes.verticalScrollBar().maximum()
            )
        )
    # ==========================================
    # ERROR
    # ==========================================

    def mostrar_error(
        self,
        mensaje
    ):

        self._timer_streaming.stop()
        self.actualizar_streaming()

        if hasattr(self, "burbuja_ia"):
            self.burbuja_ia.actualizar_contenido(
                self._texto_respuesta
            )

        burbuja_error = ChatBubble(
            f"⚠️ Error: {mensaje}",
            "assistant"
        )

        self.layout_mensajes.insertWidget(
            self.layout_mensajes.count() - 1,
            burbuja_error
        )

        self.boton_enviar.setEnabled(
            True
        )

        self.entrada.setFocus()

    # ==========================================
    # NUEVA CONVERSACIÓN
    # ==========================================

    def nueva_conversacion(self):

        self.controller.limpiar_documento()

        try:

            conversation_id = (
                self.controller.nueva_conversacion()
            )

            # ==========================================
            # LIMPIAR CHAT
            # ==========================================

            while self.layout_mensajes.count() > 1:

                elemento = (
                    self.layout_mensajes.takeAt(0)
                )

                widget = elemento.widget()

                if widget is not None:

                    widget.deleteLater()

            empty_state = EmptyState()

            self.layout_mensajes.insertWidget(
                self.layout_mensajes.count() - 1,
                empty_state
            )

            self.entrada.clear()

            self.entrada.setFocus()

            self.cargar_conversaciones()

            # Seleccionar visualmente la conversación activa
            for i in range(self.historial.count()):

                elemento = self.historial.item(i)

                if elemento.data(Qt.UserRole) == conversation_id:

                    self.historial.setCurrentRow(i)

                    break

        except Exception as e:

            self.mostrar_error(
                str(e)
            )

    # ==========================================
    # ABRIR MEMORIAS
    # ==========================================

    def abrir_memorias(self):

        if self.memory_window is None:

            self.memory_window = MemoryWindow(
                self.controller
            )

        self.memory_window.show()

        self.memory_window.raise_()

        self.memory_window.activateWindow()

    # ==========================================
    # CARGAR CONVERSACIONES
    # ==========================================
    def seleccionar_conversacion_activa(self):

        conversation_id = self.controller.conversation_id

        if conversation_id is None:
            return

        for i in range(self.historial.count()):

            elemento = self.historial.item(i)

            if elemento.data(Qt.UserRole) == conversation_id:

                self.historial.setCurrentRow(i)

                break


    def cargar_conversaciones(self):

        try:

            conversaciones = (
                self.controller.listar_conversaciones()
            )

            self.historial.clear()

            for conversacion in conversaciones:

                conversation_id = conversacion[0]
                titulo = conversacion[1]

                self.historial.addItem(
                    f"💬  {titulo}"
                )

                elemento = (
                    self.historial.item(
                        self.historial.count() - 1
                    )
                )

                elemento.setData(
                    Qt.UserRole,
                    conversation_id
                )

        except Exception as e:

            self.mostrar_error(
                str(e)
            )

    # ==========================================
    # SELECCIONAR CONVERSACIÓN
    # ==========================================

    def seleccionar_conversacion(
        self,
        item
    ):

        try:

            conversation_id = item.data(
                Qt.UserRole
            )

            resultado = (
                self.controller.abrir_conversacion(
                    conversation_id
                )
            )

            if resultado is None:

                return

            # ==========================================
            # LIMPIAR MENSAJES
            # ==========================================

            while self.layout_mensajes.count():

                elemento = self.layout_mensajes.takeAt(0)

                widget = elemento.widget()

                if widget is not None:
                    widget.deleteLater()

            # Restaurar el espacio flexible al final.
            self.layout_mensajes.addStretch()

            # ==========================================
            # CARGAR MENSAJES Y PDF EN ORDEN CRONOLÓGICO
            # ==========================================

            db = self.controller.local_ai.db

            # Recuperar todos los mensajes con sus IDs,
            # únicamente para reconstruir la interfaz.
            with db.connect() as connection:

                mensajes_db = connection.execute("""
                    SELECT id, role, content
                    FROM messages
                    WHERE conversation_id = ?
                    ORDER BY id ASC
                """, (conversation_id,)).fetchall()

            archivos = db.get_conversation_files(
                conversation_id
            )

            # Agrupar los PDF por el ID del último mensaje
            # existente cuando se adjuntaron.
            archivos_por_mensaje = {}
            archivos_sin_referencia = []

            for archivo in archivos:

                archivo_id = archivo[0]
                nombre_archivo = archivo[2]
                caracteres = archivo[4]
                after_message_id = archivo[6]

                datos_archivo = (
                    nombre_archivo,
                    caracteres
                )

                if after_message_id is None:

                    # Compatibilidad con PDF antiguos.
                    archivos_sin_referencia.append(
                        datos_archivo
                    )

                else:

                    archivos_por_mensaje.setdefault(
                        after_message_id,
                        []
                    ).append(datos_archivo)

            def agregar_burbuja_pdf(
                nombre_archivo,
                caracteres
            ):

                burbuja_archivo = ChatBubble(
                    f"📄  {nombre_archivo}\n"
                    f"PDF · {caracteres:,} caracteres",
                    "user"
                )

                self.layout_mensajes.insertWidget(
                    self.layout_mensajes.count() - 1,
                    burbuja_archivo
                )

            # Recorrer los mensajes en el orden original.
            for mensaje in mensajes_db:

                mensaje_id = mensaje[0]
                role = mensaje[1]
                content = mensaje[2]

                if role in ("user", "assistant"):

                    burbuja = ChatBubble(
                        content,
                        role
                    )

                    self.layout_mensajes.insertWidget(
                        self.layout_mensajes.count() - 1,
                        burbuja
                    )

                # Mostrar los archivos adjuntados después
                # de este mensaje.
                for nombre_archivo, caracteres in (
                    archivos_por_mensaje.get(
                        mensaje_id,
                        []
                    )
                ):

                    agregar_burbuja_pdf(
                        nombre_archivo,
                        caracteres
                    )

            # Los archivos anteriores a esta mejora no
            # tienen referencia de mensaje.
            for nombre_archivo, caracteres in (
                archivos_sin_referencia
            ):

                agregar_burbuja_pdf(
                    nombre_archivo,
                    caracteres
                )

            self.entrada.clear()
            self.entrada.setFocus()

            # ==========================================
            # IR AL FINAL
            # ==========================================

            barra = (
                self.area_mensajes.verticalScrollBar()
            )

            barra.setValue(
                barra.maximum()
            )

        except Exception as e:

            self.mostrar_error(
                str(e)
            )

    # ==========================================
    # ELIMINAR CONVERSACIÓN
    # ==========================================

    def eliminar_conversacion(self):

        item = self.historial.currentItem()

        if item is None:

            dialogo = ConfirmDialog(
                "💬 Conversación",
                "Selecciona una conversación primero.",
                texto_confirmar="Entendido"
            )

            dialogo.exec()

            return

        conversation_id = item.data(
            Qt.UserRole
        )

        # ==========================================
        # OBTENER TÍTULO DE LA CONVERSACIÓN
        # ==========================================

        titulo = item.text()

        if "  " in titulo:

            titulo = titulo.split(
                "  ",
                1
            )[1]

        # ==========================================
        # CONFIRMAR ELIMINACIÓN
        # ==========================================

        dialogo = ConfirmDialog(
            "🗑️ Eliminar conversación",
            "¿Quieres eliminar esta conversación?",
            f"«{titulo}»\n\nEsta acción no se puede deshacer.",
            texto_confirmar="Eliminar",
            texto_cancelar="Cancelar",
            peligro=True
        )

        if dialogo.exec() != QDialog.DialogCode.Accepted:
            return

        try:

            eliminado = (
                self.controller.eliminar_conversacion(
                    conversation_id
                )
            )

            if not eliminado:

                QMessageBox.warning(
                    self,
                    "Eliminar conversación",
                    "No se pudo encontrar la conversación."
                )

                return

            # ==========================================
            # SI ERA LA CONVERSACIÓN ACTUAL
            # ==========================================

            if (
                self.controller.conversation_id
                == conversation_id
            ):

                self.controller.conversation_id = None

                self.controller.messages = [
                    self.controller.system_message.copy()
                ]

                while self.layout_mensajes.count() > 1:

                    elemento = (
                        self.layout_mensajes.takeAt(0)
                    )

                    widget = elemento.widget()

                    if widget is not None:

                        widget.deleteLater()

                empty_state = EmptyState()

                self.layout_mensajes.insertWidget(
                    self.layout_mensajes.count() - 1,
                    empty_state
                )

            self.cargar_conversaciones()

        except Exception as e:

            self.mostrar_error(
                str(e)
            )
    # ==========================================
    # RENOMBRAR CONVERSACIÓN
    # ==========================================

    def renombrar_conversacion(self):

        item = self.historial.currentItem()

        if item is None:

            dialogo = ConfirmDialog(
                "💬 Conversación",
                "Selecciona una conversación primero.",
                texto_confirmar="Entendido"
            )

            dialogo.exec()

            return

        conversation_id = item.data(
            Qt.UserRole
        )

        conversacion = None

        for i in range(
            self.historial.count()
        ):

            elemento = self.historial.item(i)

            if (
                elemento.data(Qt.UserRole)
                == conversation_id
            ):

                texto = elemento.text()

                if "  " in texto:

                    titulo_actual = texto.split(
                        "  ",
                        1
                    )[1]

                else:

                    titulo_actual = texto

                break

        else:

            QMessageBox.warning(
                self,
                "Renombrar conversación",
                "No se pudo encontrar la conversación."
            )

            return

        dialogo = RenameDialog(
            titulo_actual
        )

        if dialogo.exec() != QDialog.DialogCode.Accepted:
            return

        nuevo_titulo = dialogo.nombre

        try:

            actualizado = (
                self.controller.renombrar_conversacion(
                    conversation_id,
                    nuevo_titulo
                )
            )

            if actualizado is False:

                QMessageBox.warning(
                    self,
                    "Renombrar conversación",
                    "No se pudo cambiar el nombre."
                )

                return

            item.setText(
                f"💬  {nuevo_titulo}"
            )

        except Exception as e:

            self.mostrar_error(
                str(e)
            )

    # ==========================================
    # ADJUNTAR ARCHIVO
    # ==========================================

    def adjuntar_archivo(self):

        ruta, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo",
            "",
            "Archivos PDF (*.pdf)"
        )

        if not ruta:
            return

        try:

            documento = self.controller.adjuntar_pdf(
                ruta
            )

            texto = documento["texto"]

            # ==========================================
            # OBTENER NOMBRE DEL ARCHIVO
            # ==========================================

            import os

            nombre_archivo = documento["nombre"]

            # ==========================================
            # MOSTRAR ARCHIVO EN EL CHAT
            # ==========================================

            burbuja_archivo = ChatBubble(
                f"📄  {nombre_archivo}\n"
                f"PDF · {len(texto):,} caracteres",
                "user"
            )

            self.layout_mensajes.insertWidget(
                self.layout_mensajes.count() - 1,
                burbuja_archivo
            )

            # ==========================================
            # INFORMACIÓN EN TERMINAL
            # ==========================================

            print("=" * 60)
            print("PDF SELECCIONADO")
            print("=" * 60)
            print(f"Archivo: {ruta}")
            print(f"Nombre: {nombre_archivo}")
            print(f"Caracteres: {len(texto)}")
            print("=" * 60)

        except Exception as e:

            self.mostrar_error(
                str(e)
            )


# ==========================================
# INICIAR GUI
# ==========================================

def iniciar_gui():

    app = QApplication([])

    ventana = MainWindow()

    ventana.show()

    app.exec()


# ==========================================
# EJECUTAR
# ==========================================

if __name__ == "__main__":

    iniciar_gui()