# ==========================================
# DIÁLOGO PERSONALIZADO
# ==========================================

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QSpinBox,
)


# ==========================================
# DIÁLOGO DE CONFIRMACIÓN
# ==========================================

class ConfirmDialog(QDialog):

    def __init__(
        self,
        titulo,
        mensaje,
        detalle="",
        texto_confirmar="Confirmar",
        texto_cancelar="Cancelar",
        peligro=False
    ):

        super().__init__()

        self.resultado = False

        self.setWindowTitle(
            titulo
        )

        self.setModal(
            True
        )

        self.setFixedWidth(
            420
        )

        self.crear_interfaz(
            titulo,
            mensaje,
            detalle,
            texto_confirmar,
            texto_cancelar,
            peligro
        )

    # ==========================================
    # CREAR INTERFAZ
    # ==========================================

    def crear_interfaz(
        self,
        titulo,
        mensaje,
        detalle,
        texto_confirmar,
        texto_cancelar,
        peligro
    ):

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            24,
            22,
            24,
            20
        )

        layout.setSpacing(
            10
        )

        # ==========================================
        # TITULO
        # ==========================================

        etiqueta_titulo = QLabel(
            titulo
        )

        etiqueta_titulo.setStyleSheet(
            """
            QLabel {
                color: #222222;
                font-size: 18px;
                font-weight: 600;
            }
            """
        )

        # ==========================================
        # MENSAJE
        # ==========================================

        etiqueta_mensaje = QLabel(
            mensaje
        )

        etiqueta_mensaje.setWordWrap(
            True
        )

        etiqueta_mensaje.setStyleSheet(
            """
            QLabel {
                color: #444444;
                font-size: 14px;
            }
            """
        )

        # ==========================================
        # DETALLE
        # ==========================================

        etiqueta_detalle = QLabel(
            detalle
        )

        etiqueta_detalle.setWordWrap(
            True
        )

        etiqueta_detalle.setStyleSheet(
            """
            QLabel {
                color: #777777;
                font-size: 13px;
                padding: 6px 0px;
            }
            """
        )

        layout.addWidget(
            etiqueta_titulo
        )

        layout.addWidget(
            etiqueta_mensaje
        )

        if detalle:

            layout.addWidget(
                etiqueta_detalle
            )

        # ==========================================
        # BOTONES
        # ==========================================

        panel_botones = QHBoxLayout()

        panel_botones.setSpacing(
            8
        )

        panel_botones.addStretch()

        boton_cancelar = QPushButton(
            texto_cancelar
        )

        boton_cancelar.setFixedHeight(
            38
        )

        boton_cancelar.setStyleSheet(
            """
            QPushButton {
                background-color: #eeeeef;
                color: #333333;
                border: 1px solid #dddddf;
                border-radius: 9px;
                padding: 0px 16px;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #e5e5e7;
            }

            QPushButton:pressed {
                background-color: #dcdcdf;
            }
            """
        )

        boton_confirmar = QPushButton(
            texto_confirmar
        )

        boton_confirmar.setFixedHeight(
            38
        )

        if peligro:

            boton_confirmar.setStyleSheet(
                """
                QPushButton {
                    background-color: #dc3545;
                    color: white;
                    border: none;
                    border-radius: 9px;
                    padding: 0px 16px;
                    font-size: 14px;
                    font-weight: 600;
                }

                QPushButton:hover {
                    background-color: #c82333;
                }

                QPushButton:pressed {
                    background-color: #b21f2d;
                }
                """
            )

        else:

            boton_confirmar.setStyleSheet(
                """
                QPushButton {
                    background-color: #2b7cff;
                    color: white;
                    border: none;
                    border-radius: 9px;
                    padding: 0px 16px;
                    font-size: 14px;
                    font-weight: 600;
                }

                QPushButton:hover {
                    background-color: #1f6be0;
                }

                QPushButton:pressed {
                    background-color: #1859bd;
                }
                """
            )

        panel_botones.addWidget(
            boton_cancelar
        )

        panel_botones.addWidget(
            boton_confirmar
        )

        layout.addLayout(
            panel_botones
        )

        boton_cancelar.clicked.connect(
            self.reject
        )

        boton_confirmar.clicked.connect(
            self.confirmar
        )

    # ==========================================
    # CONFIRMAR
    # ==========================================

    def confirmar(self):

        self.resultado = True

        self.accept()

# ==========================================
# DIÁLOGO PARA RENOMBRAR
# ==========================================

from PySide6.QtWidgets import QLineEdit


class RenameDialog(QDialog):

    def __init__(
        self,
        nombre_actual
    ):

        super().__init__()

        self.nombre = ""

        self.setWindowTitle(
            "✏️ Renombrar conversación"
        )

        self.setModal(
            True
        )

        self.setFixedWidth(
            420
        )

        self.crear_interfaz(
            nombre_actual
        )

    # ==========================================
    # CREAR INTERFAZ
    # ==========================================

    def crear_interfaz(
        self,
        nombre_actual
    ):

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            24,
            22,
            24,
            20
        )

        layout.setSpacing(
            10
        )

        # ==========================================
        # TITULO
        # ==========================================

        titulo = QLabel(
            "✏️ Renombrar conversación"
        )

        titulo.setStyleSheet(
            """
            QLabel {
                color: #222222;
                font-size: 18px;
                font-weight: 600;
            }
            """
        )

        # ==========================================
        # DESCRIPCIÓN
        # ==========================================

        descripcion = QLabel(
            "Cambia el nombre de esta conversación."
        )

        descripcion.setStyleSheet(
            """
            QLabel {
                color: #666666;
                font-size: 14px;
            }
            """
        )

        # ==========================================
        # CAMPO DE TEXTO
        # ==========================================

        self.entrada = QLineEdit()

        self.entrada.setText(
            nombre_actual
        )

        self.entrada.selectAll()

        self.entrada.setFixedHeight(
            40
        )

        self.entrada.setStyleSheet(
            """
            QLineEdit {
                background-color: #f5f5f5;
                color: #222222;
                border: 1px solid #dddddd;
                border-radius: 9px;
                padding: 0px 12px;
                font-size: 14px;
            }

            QLineEdit:focus {
                border: 1px solid #2b7cff;
                background-color: #ffffff;
            }
            """
        )

        # ==========================================
        # BOTONES
        # ==========================================

        panel_botones = QHBoxLayout()

        panel_botones.setSpacing(
            8
        )

        panel_botones.addStretch()

        boton_cancelar = QPushButton(
            "Cancelar"
        )

        boton_cancelar.setFixedHeight(
            38
        )

        boton_cancelar.setStyleSheet(
            """
            QPushButton {
                background-color: #eeeeef;
                color: #333333;
                border: 1px solid #dddddf;
                border-radius: 9px;
                padding: 0px 16px;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #e5e5e7;
            }

            QPushButton:pressed {
                background-color: #dcdcdf;
            }
            """
        )

        boton_guardar = QPushButton(
            "Guardar"
        )

        boton_guardar.setFixedHeight(
            38
        )

        boton_guardar.setStyleSheet(
            """
            QPushButton {
                background-color: #2b7cff;
                color: white;
                border: none;
                border-radius: 9px;
                padding: 0px 16px;
                font-size: 14px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #1f6be0;
            }

            QPushButton:pressed {
                background-color: #1859bd;
            }
            """
        )

        panel_botones.addWidget(
            boton_cancelar
        )

        panel_botones.addWidget(
            boton_guardar
        )

        # ==========================================
        # AGREGAR ELEMENTOS
        # ==========================================

        layout.addWidget(
            titulo
        )

        layout.addWidget(
            descripcion
        )

        layout.addWidget(
            self.entrada
        )

        layout.addSpacing(
            8
        )

        layout.addLayout(
            panel_botones
        )

        # ==========================================
        # EVENTOS
        # ==========================================

        boton_cancelar.clicked.connect(
            self.reject
        )

        boton_guardar.clicked.connect(
            self.guardar
        )

        self.entrada.returnPressed.connect(
            self.guardar
        )

    # ==========================================
    # GUARDAR
    # ==========================================

    def guardar(self):

        nombre = self.entrada.text().strip()

        if not nombre:

            return

        self.nombre = nombre

        self.accept()

# ==========================================
# DIÁLOGO PARA EDITAR MEMORIA
# ==========================================

class MemoryEditDialog(QDialog):

    def __init__(
        self,
        category,
        key,
        value,
        importance
    ):

        super().__init__()

        self.categoria = ""
        self.clave = ""
        self.valor = ""
        self.importancia = importance

        self.setWindowTitle(
            "🧠 Editar memoria"
        )

        self.setModal(True)

        self.setFixedWidth(
            460
        )

        self.crear_interfaz(
            category,
            key,
            value,
            importance
        )

    # ==========================================
    # CREAR INTERFAZ
    # ==========================================

    def crear_interfaz(
        self,
        category,
        key,
        value,
        importance
    ):

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            24,
            22,
            24,
            20
        )

        layout.setSpacing(
            10
        )

        titulo = QLabel(
            "🧠 Editar memoria"
        )

        titulo.setStyleSheet(
            """
            QLabel {
                color: #222222;
                font-size: 18px;
                font-weight: 600;
            }
            """
        )

        descripcion = QLabel(
            "Modifica la información que Local AI recuerda."
        )

        descripcion.setStyleSheet(
            """
            QLabel {
                color: #777777;
                font-size: 13px;
            }
            """
        )

        # ==========================================
        # CATEGORÍA
        # ==========================================

        etiqueta_categoria = QLabel(
            "Categoría"
        )

        self.campo_categoria = QLineEdit(
            category
        )

        # ==========================================
        # CLAVE
        # ==========================================

        etiqueta_clave = QLabel(
            "Clave"
        )

        self.campo_clave = QLineEdit(
            key
        )

        # ==========================================
        # VALOR
        # ==========================================

        etiqueta_valor = QLabel(
            "Valor"
        )

        self.campo_valor = QLineEdit(
            value
        )

        # ==========================================
        # IMPORTANCIA
        # ==========================================

        etiqueta_importancia = QLabel(
            "Importancia"
        )

        self.campo_importancia = QSpinBox()

        self.campo_importancia.setRange(
            1,
            5
        )

        self.campo_importancia.setValue(
            importance
        )

        # ==========================================
        # ESTILO CAMPOS
        # ==========================================

        estilo_campo = """
            QLineEdit {
                background-color: #f5f5f5;
                border: 1px solid #dddddd;
                border-radius: 8px;
                padding: 8px 10px;
                font-size: 14px;
                color: #333333;
            }

            QLineEdit:focus {
                background-color: #ffffff;
                border: 1px solid #2b7cff;
            }

            QSpinBox {
                background-color: #f5f5f5;
                border: 1px solid #dddddd;
                border-radius: 8px;
                padding: 6px 8px;
                font-size: 14px;
                color: #333333;
            }

            QSpinBox:focus {
                background-color: #ffffff;
                border: 1px solid #2b7cff;
            }

            QSpinBox::up-button,
            QSpinBox::down-button {
                width: 22px;
                border-left: 1px solid #dddddd;
                background-color: #eeeeef;
            }

            QSpinBox::up-button:hover,
            QSpinBox::down-button:hover {
                background-color: #e0e0e2;
            }
        """

        self.campo_categoria.setStyleSheet(
            estilo_campo
        )

        self.campo_clave.setStyleSheet(
            estilo_campo
        )

        self.campo_valor.setStyleSheet(
            estilo_campo
        )

        self.campo_importancia.setStyleSheet(
            estilo_campo
        )

        # ==========================================
        # BOTONES
        # ==========================================

        botones = QHBoxLayout()

        botones.addStretch()

        boton_cancelar = QPushButton(
            "Cancelar"
        )

        boton_guardar = QPushButton(
            "Guardar"
        )

        boton_cancelar.setFixedHeight(
            38
        )

        boton_guardar.setFixedHeight(
            38
        )

        boton_cancelar.setStyleSheet(
            """
            QPushButton {
                background-color: #eeeeef;
                color: #333333;
                border: 1px solid #dddddf;
                border-radius: 8px;
                padding: 0px 16px;
                font-size: 14px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #e5e5e7;
            }
            """
        )

        boton_guardar.setStyleSheet(
            """
            QPushButton {
                background-color: #2b7cff;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0px 18px;
                font-size: 14px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #2169d5;
            }
            """
        )

        botones.addWidget(
            boton_cancelar
        )

        botones.addWidget(
            boton_guardar
        )

        # ==========================================
        # AGREGAR ELEMENTOS
        # ==========================================

        layout.addWidget(
            titulo
        )

        layout.addWidget(
            descripcion
        )

        layout.addSpacing(
            6
        )

        layout.addWidget(
            etiqueta_categoria
        )

        layout.addWidget(
            self.campo_categoria
        )

        layout.addWidget(
            etiqueta_clave
        )

        layout.addWidget(
            self.campo_clave
        )

        layout.addWidget(
            etiqueta_valor
        )

        layout.addWidget(
            self.campo_valor
        )

        layout.addWidget(
            etiqueta_importancia
        )

        layout.addWidget(
            self.campo_importancia
        )

        layout.addSpacing(
            8
        )

        layout.addLayout(
            botones
        )

        boton_cancelar.clicked.connect(
            self.reject
        )

        boton_guardar.clicked.connect(
            self.guardar
        )

    # ==========================================
    # GUARDAR
    # ==========================================

    def guardar(self):

        categoria = self.campo_categoria.text().strip()
        clave = self.campo_clave.text().strip()
        valor = self.campo_valor.text().strip()

        if not categoria or not clave or not valor:
            return

        self.categoria = categoria
        self.clave = clave
        self.valor = valor
        self.importancia = (
            self.campo_importancia.value()
        )

        self.accept()