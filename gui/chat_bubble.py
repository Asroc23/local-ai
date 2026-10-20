
# ==========================================
# BURBUJA DE CHAT
# ==========================================

import re
import markdown
import html as html_lib

from PySide6.QtCore import Qt, QTimer, QMimeData
from PySide6.QtGui import QPixmap, QTextDocument, QTextCursor
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QTextBrowser,
    QHBoxLayout,
    QVBoxLayout,
    QSizePolicy,
    QTextEdit,
    QPlainTextEdit,
    QFrame,
    QPushButton,
    QApplication,
)


def normalizar_tablas_markdown(texto):
    lineas = texto.splitlines()
    resultado = []
    i = 0

    def separar_celdas(linea):
        return [
            celda.strip()
            for celda in linea.strip().strip("|").split("|")
        ]

    def es_separador(linea):
        celdas = separar_celdas(linea)

        return (
            len(celdas) >= 2
            and all(
                re.fullmatch(r":?-{3,}:?", celda)
                for celda in celdas
            )
        )

    while i < len(lineas):
        linea = lineas[i].strip()

        # Detectar bloques de código que contienen tablas Markdown.
        if linea.startswith("```"):
            inicio_bloque = i
            etiqueta = linea[3:].strip().lower()

            j = i + 1

            while (
                j < len(lineas)
                and not lineas[j].strip().startswith("```")
            ):
                j += 1

            if j < len(lineas):
                contenido_bloque = lineas[i + 1:j]

                contiene_tabla = any(
                    k + 1 < len(contenido_bloque)
                    and "|" in contenido_bloque[k]
                    and es_separador(
                        contenido_bloque[k + 1]
                    )
                    for k in range(len(contenido_bloque))
                )

                if contiene_tabla and etiqueta in (
                    "", "markdown", "md", "text"
                ):
                    lineas = (
                        lineas[:inicio_bloque]
                        + contenido_bloque
                        + lineas[j + 1:]
                    )

                    i = inicio_bloque
                    continue

        # Detectar un encabezado seguido de su separador.
        if (
            i + 1 < len(lineas)
            and "|" in lineas[i]
            and es_separador(lineas[i + 1])
        ):
            encabezado = separar_celdas(lineas[i])
            separador = separar_celdas(lineas[i + 1])

            if len(encabezado) == len(separador):
                resultado.append(
                    "| " + " | ".join(encabezado) + " |"
                )

                resultado.append(
                    "| " + " | ".join(separador) + " |"
                )

                i += 2

                while i < len(lineas):
                    actual = lineas[i].strip()

                    if not actual or "|" not in actual:
                        break

                    celdas = separar_celdas(actual)

                    if len(celdas) != len(encabezado):
                        break

                    resultado.append(
                        "| " + " | ".join(celdas) + " |"
                    )

                    i += 1

                resultado.append("")
                continue

        resultado.append(lineas[i])
        i += 1

    return "\n".join(resultado)

class BloqueCodigo(QFrame):

    def __init__(self, codigo, lenguaje="Código", parent=None):
        super().__init__(parent)

        self.codigo = codigo
        self.lenguaje = lenguaje.upper()

        self.setObjectName("bloqueCodigo")
        self.setStyleSheet("""
            QFrame#bloqueCodigo {
                background-color: #1e1e1e;
                border: 1px solid #3c3c3c;
                border-radius: 8px;
            }

            QLabel {
                color: #d4d4d4;
                border: none;
                font-size: 11px;
                font-weight: 600;
            }

            QPushButton {
                background-color: #303030;
                color: #f1f1f1;
                border: 1px solid #505050;
                border-radius: 5px;
                padding: 4px 9px;
                font-size: 11px;
            }

            QPushButton:hover {
                background-color: #454545;
            }

            QPlainTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: none;
                padding: 8px;
                font-family: monospace;
                font-size: 13px;
                selection-background-color: #264f78;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 8)
        layout.setSpacing(4)

        encabezado = QHBoxLayout()

        etiqueta = QLabel(self.lenguaje)

        self.boton_copiar = QPushButton("Copiar código")
        self.boton_copiar.setCursor(
            Qt.CursorShape.PointingHandCursor
        )
        self.boton_copiar.clicked.connect(
            self.copiar_codigo
        )

        encabezado.addWidget(etiqueta)
        encabezado.addStretch()
        encabezado.addWidget(self.boton_copiar)

        layout.addLayout(encabezado)

        self.editor = QPlainTextEdit()
        self.editor.setReadOnly(True)
        self.editor.setPlainText(self.codigo)
        self.editor.setLineWrapMode(
            QPlainTextEdit.LineWrapMode.NoWrap
        )
        self.editor.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.editor.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )


        # Calcular la altura según la cantidad de líneas.
        # Así el código será legible sin ocupar espacio
        # innecesario en bloques pequeños.
        cantidad_lineas = max(
            1,
            self.editor.document().blockCount()
        )

        altura_linea = self.editor.fontMetrics().lineSpacing()

        altura_codigo = (
            cantidad_lineas * altura_linea + 28
        )

        altura_codigo = max(
            100,
            min(altura_codigo, 420)
        )

        self.editor.setMinimumHeight(altura_codigo)
        self.editor.setMaximumHeight(altura_codigo)

        layout.addWidget(self.editor)


    def copiar_codigo(self):
        QApplication.clipboard().setText(self.codigo)

        self.boton_copiar.setText("✓ Copiado")

        QTimer.singleShot(
            1800,
            self.restaurar_boton
        )

    def restaurar_boton(self):
        self.boton_copiar.setText("Copiar código")


class MensajeMarkdown(QWidget):

    ALTURA_MINIMA = 42
    ALTURA_MAXIMA = 10000

    def __init__(self, parent=None):
        super().__init__(parent)

        self.html_renderizado = ""
        self.bloques_codigo = []

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )

        self.layout_contenido = QVBoxLayout(self)
        self.layout_contenido.setContentsMargins(0, 0, 0, 0)
        self.layout_contenido.setSpacing(8)
        self.streaming_browser = None

    def limpiar_contenido(self):
        while self.layout_contenido.count():
            elemento = self.layout_contenido.takeAt(0)
            widget = elemento.widget()

            if widget is not None:
                widget.deleteLater()

        self.bloques_codigo.clear()
        self.streaming_browser = None

    def agregar_texto_streaming(self, texto):
        """Añade texto sin reconstruir todo el Markdown."""

        if not texto:
            return

        if self.streaming_browser is None:
            self.limpiar_contenido()

            navegador = QTextBrowser(self)

            navegador.setReadOnly(True)
            navegador.setOpenExternalLinks(False)

            navegador.setTextInteractionFlags(
                Qt.TextInteractionFlag.TextSelectableByMouse
            )

            navegador.setVerticalScrollBarPolicy(
                Qt.ScrollBarPolicy.ScrollBarAlwaysOff
            )

            navegador.setHorizontalScrollBarPolicy(
                Qt.ScrollBarPolicy.ScrollBarAlwaysOff
            )

            navegador.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Preferred
            )

            navegador.document().setDocumentMargin(4)

            self.streaming_browser = navegador

            self.layout_contenido.addWidget(navegador)

        navegador = self.streaming_browser

        cursor = navegador.textCursor()

        cursor.movePosition(
            QTextCursor.MoveOperation.End
        )

        cursor.insertText(texto)

        navegador.setTextCursor(cursor)

        # Ajustar la altura sin recrear el navegador.
        self.ajustar_fragmento(navegador)

    def formatear_tablas(self, html):

        def formatear_tabla(match):
            tabla = match.group(0)

            tabla = re.sub(
                r"<table\b[^>]*>",
                '<table border="1" cellspacing="0" cellpadding="4" '
                'width="100%" '
                'style="width:100%; border-collapse:collapse; '
                'table-layout:fixed; border:1px solid #cbd5e1;">',
                tabla,
                count=1,
                flags=re.IGNORECASE,
            )

            tabla = re.sub(
                r"<th\b[^>]*>",
                '<th bgcolor="#dbeafe" '
                'style="background-color:#dbeafe; '
                'color:#1e3a8a; font-weight:bold; '
                'border:1px solid #bfdbfe; padding:4px;">',
                tabla,
                flags=re.IGNORECASE,
            )

            tabla = re.sub(
                r"<td\b[^>]*>",
                '<td bgcolor="#ffffff" '
                'style="background-color:#ffffff; '
                'color:#334155; '
                'border:1px solid #e2e8f0; padding:4px;">',
                tabla,
                flags=re.IGNORECASE,
            )

            return tabla

        return re.sub(
            r"<table\b[^>]*>.*?</table>",
            formatear_tabla,
            html,
            flags=re.IGNORECASE | re.DOTALL,
        )

    def crear_fragmento_texto(self, contenido):

        if not contenido.strip():
            return ""

        html = markdown.markdown(
            contenido,
            extensions=[
                "tables",
                "fenced_code",
                "nl2br",
            ],
        )

        html = self.formatear_tablas(html)

        navegador = QTextBrowser(self)

        navegador.setReadOnly(True)
        navegador.setOpenExternalLinks(False)

        navegador.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        navegador.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        navegador.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        navegador.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )

        navegador.document().setDocumentMargin(4)
        navegador.setHtml(html)

        self.layout_contenido.addWidget(navegador)

        QTimer.singleShot(
            0,
            lambda navegador=navegador:
                self.ajustar_fragmento(navegador)
        )

        return html

    def ajustar_fragmento(self, navegador):

        if navegador is None:
            return

        ancho = navegador.viewport().width()

        if ancho <= 0:
            return

        documento = navegador.document()
        documento.setTextWidth(ancho)

        altura = int(documento.size().height()) + 24

        altura = max(
            self.ALTURA_MINIMA,
            altura
        )

        navegador.setMinimumHeight(altura)
        navegador.setMaximumHeight(altura)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        QTimer.singleShot(
            0,
            self.ajustar_todos_fragmentos
        )

    def ajustar_todos_fragmentos(self):

        for indice in range(self.layout_contenido.count()):
            elemento = self.layout_contenido.itemAt(indice)
            widget = elemento.widget()

            if isinstance(widget, QTextBrowser):
                self.ajustar_fragmento(widget)

    def establecer_markdown(self, contenido):

        contenido = normalizar_tablas_markdown(
            contenido
        )

        self.limpiar_contenido()

        fragmentos_html = []
        posicion = 0

        # Detectar bloques Markdown delimitados por tres
        # acentos graves, conservando el código original.
        patron = re.compile(
            r"```([^\n`]*)\n(.*?)```",
            re.DOTALL
        )

        for coincidencia in patron.finditer(contenido):

            texto_anterior = contenido[
                posicion:coincidencia.start()
            ]

            html_texto = self.crear_fragmento_texto(
                texto_anterior
            )

            if html_texto:
                fragmentos_html.append(html_texto)

            lenguaje = (
                coincidencia.group(1).strip()
                or "Código"
            )

            codigo = coincidencia.group(2)

            # Crear un widget independiente para este bloque.
            bloque = BloqueCodigo(
                codigo=codigo,
                lenguaje=lenguaje,
                parent=self
            )

            self.bloques_codigo.append(bloque)

            self.layout_contenido.addWidget(bloque)

            # Mantener una representación HTML para que las
            # funciones existentes puedan detectar el código.
            lenguaje_html = html_lib.escape(lenguaje)

            codigo_html = html_lib.escape(codigo)

            fragmentos_html.append(
                '<pre><code class="language-'
                + lenguaje_html
                + '">'
                + codigo_html
                + '</code></pre>'
            )

            posicion = coincidencia.end()

        # Procesar el texto que aparece después del último bloque.
        texto_final = contenido[posicion:]

        html_final = self.crear_fragmento_texto(
            texto_final
        )

        if html_final:
            fragmentos_html.append(html_final)

        self.html_renderizado = "\n".join(
            fragmentos_html
        )

        QTimer.singleShot(
            0,
            self.ajustar_todos_fragmentos
        )


class ChatBubble(QWidget):

    def __init__(self, content, role):
        super().__init__()

        self.content = str(content)
        self.role = role

        self.boton_copiar_tabla = None

        self.crear_interfaz()

    # ==========================================
    # ACTUALIZAR CONTENIDO
    # ==========================================


    def actualizar_contenido(self, contenido):

        self.content = str(contenido)

        self.mensaje.establecer_markdown(
            self.content
        )

        # Mostrar el botón de copiar tabla únicamente
        # cuando el mensaje contiene al menos una tabla.
        if (
            self.role != "user"
            and self.boton_copiar_tabla is not None
        ):
            contiene_tabla = bool(
                re.search(
                    r"<table\b",
                    self.mensaje.html_renderizado,
                    flags=re.IGNORECASE,
                )
            )

            self.boton_copiar_tabla.setVisible(
                contiene_tabla
            )

    # ==========================================
    # COPIAR TABLA
    # ==========================================

    def copiar_tabla(self):

        if self.role == "user":
            return

        html = self.mensaje.html_renderizado

        coincidencia = re.search(
            r"<table\b[^>]*>.*?</table>",
            html,
            flags=re.IGNORECASE | re.DOTALL,
        )

        if not coincidencia:
            return

        tabla_html = coincidencia.group(0)

        # Generar texto alternativo para aplicaciones
        # que no acepten el formato HTML del portapapeles.
        documento = QTextDocument()
        documento.setHtml(tabla_html)

        texto_plano = documento.toPlainText()

        # Preparar los dos formatos en el portapapeles.
        datos = QMimeData()
        datos.setHtml(tabla_html)
        datos.setText(texto_plano)

        QApplication.clipboard().setMimeData(datos)

        self.boton_copiar_tabla.setText("✓ Copiada")

        QTimer.singleShot(
            1800,
            self.restaurar_texto_boton
        )

    def restaurar_texto_boton(self):

        if self.boton_copiar_tabla is not None:
            self.boton_copiar_tabla.setText(
                "Copiar tabla"
            )

    # ==========================================
    # CREAR INTERFAZ
    # ==========================================

    def crear_interfaz(self):

        layout_principal = QHBoxLayout(self)

        layout_principal.setContentsMargins(
            24, 8, 24, 8
        )

        contenedor = QVBoxLayout()

        contenedor.setContentsMargins(
            0, 0, 0, 0
        )

        contenedor.setSpacing(4)

        # ==========================================
        # NOMBRE E ICONO
        # ==========================================

        nombre = QLabel(
            "Tú" if self.role == "user" else "Local AI"
        )

        icono = QLabel()

        pixmap = QPixmap("assets/local_ai.png")

        if not pixmap.isNull():
            icono.setPixmap(
                pixmap.scaled(
                    28,
                    28,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )

        # ==========================================
        # CONTENIDO
        # ==========================================

        self.mensaje = MensajeMarkdown()

        self.mensaje.setObjectName("mensaje")

        self.mensaje.setMinimumWidth(220)
        self.mensaje.setMaximumWidth(750)

        self.mensaje.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )

        # ==========================================
        # MENSAJE DEL USUARIO
        # ==========================================

        if self.role == "user":

            nombre.setAlignment(
                Qt.AlignmentFlag.AlignRight
            )

            nombre.setStyleSheet(
                "color: #777; font-size: 12px; "
                "font-weight: 600; padding-right: 4px;"
            )

            self.mensaje.setStyleSheet("""
                QTextBrowser {
                    background-color: #f8fafc;
                    color: #1e293b;
                    border: 1px solid #e2e8f0;
                    border-radius: 12px;
                    padding: 10px;
                    font-size: 14px;
                }

                QTextBrowser a {
                    color: #2563eb;
                }

                QTextBrowser pre {
                    background-color: #1e293b;
                    color: #f8fafc;
                    padding: 10px;
                    border-radius: 8px;
                }

                QTextBrowser code {
                    font-family: monospace;
                    color: #334155;
                }

                QTextBrowser table {
                    border-collapse: collapse;
                    margin-top: 8px;
                    margin-bottom: 8px;
                }

                QTextBrowser th {
                    background-color: #dbeafe;
                    color: #1e3a8a;
                    font-weight: bold;
                    padding: 8px;
                    border: 1px solid #bfdbfe;
                }

                QTextBrowser td {
                    background-color: #ffffff;
                    color: #334155;
                    padding: 8px;
                    border: 1px solid #e2e8f0;
                }
            """)

            contenedor.addWidget(nombre)
            contenedor.addWidget(self.mensaje)

            layout_principal.addStretch()
            layout_principal.addLayout(contenedor)

        # ==========================================
        # MENSAJE DEL ASISTENTE
        # ==========================================

        else:

            nombre.setStyleSheet(
                "color: #666; font-size: 12px; "
                "font-weight: 600; padding-left: 4px;"
            )

            self.mensaje.setStyleSheet("""
                QTextBrowser {
                    background-color: #eeeeee;
                    color: #222222;
                    border: none;
                    border-radius: 16px;
                    padding: 8px;
                    font-size: 14px;
                }

                QTextBrowser a {
                    color: #1769d2;
                }

                QTextBrowser pre {
                    background-color: #252526;
                    color: #f1f1f1;
                    padding: 10px;
                    border-radius: 6px;
                }

                QTextBrowser code {
                    font-family: monospace;
                }

                QTextBrowser table {
                    border-collapse: collapse;
                }

                QTextBrowser th {
                    background-color: #d6d6d6;
                    font-weight: bold;
                }

                QTextBrowser th,
                QTextBrowser td {
                    border: 1px solid #c5c5c5;
                    padding: 5px;
                }
            """)

            # Encabezado del asistente.
            encabezado = QWidget()

            encabezado_layout = QHBoxLayout(encabezado)

            encabezado_layout.setContentsMargins(
                0, 0, 0, 0
            )

            encabezado_layout.setSpacing(6)

            encabezado_layout.addWidget(icono)
            encabezado_layout.addWidget(nombre)
            encabezado_layout.addStretch()


            # Botón para copiar la tabla.
            self.boton_copiar_tabla = QPushButton(
                "Copiar tabla"
            )

            self.boton_copiar_tabla.setCursor(
                Qt.CursorShape.PointingHandCursor
            )

            self.boton_copiar_tabla.setStyleSheet("""
                QPushButton {
                    background-color: #dbeafe;
                    color: #1e40af;
                    border: 1px solid #bfdbfe;
                    border-radius: 6px;
                    padding: 5px 10px;
                    font-size: 12px;
                    font-weight: 600;
                }

                QPushButton:hover {
                    background-color: #bfdbfe;
                }
            """)

            self.boton_copiar_tabla.clicked.connect(
                self.copiar_tabla
            )

            # Ocultarlo inicialmente si no hay una tabla.
            self.boton_copiar_tabla.hide()

            encabezado_layout.addWidget(
                self.boton_copiar_tabla
            )

            contenedor.addWidget(encabezado)
            contenedor.addWidget(self.mensaje)

            layout_principal.addLayout(contenedor)
            layout_principal.addStretch()

        # Cargar el contenido inicial.
        self.actualizar_contenido(self.content)
