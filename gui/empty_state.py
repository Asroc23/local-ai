# ==========================================
# ESTADO VACÍO DEL CHAT
# ==========================================

from PySide6.QtCore import Qt

from PySide6.QtGui import QPixmap

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)


# ==========================================
# COMPONENTE DE ESTADO VACÍO
# ==========================================

class EmptyState(QWidget):

    def __init__(self):

        super().__init__()

        self.crear_interfaz()

    # ==========================================
    # CREAR INTERFAZ
    # ==========================================

    def crear_interfaz(self):

        layout = QVBoxLayout(
            self
        )

        layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.setSpacing(
            10
        )

        # ==========================================
        # ICONO
        # ==========================================

        icono = QLabel()

        pixmap = QPixmap(
            "assets/local_ai.png"
        )

        pixmap = pixmap.scaled(
            72,
            72,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        icono.setPixmap(
            pixmap
        )

        icono.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        # ==========================================
        # TITULO
        # ==========================================

        titulo = QLabel(
            "No hay una conversación activa"
        )

        titulo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        titulo.setStyleSheet(
            """
            QLabel {
                color: #333333;
                font-size: 20px;
                font-weight: 600;
            }
            """
        )

        # ==========================================
        # DESCRIPCIÓN
        # ==========================================

        descripcion = QLabel(
            "Crea una nueva conversación para "
            "comenzar a hablar con Local AI."
        )

        descripcion.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        descripcion.setStyleSheet(
            """
            QLabel {
                color: #777777;
                font-size: 14px;
            }
            """
        )

        layout.addWidget(
            icono
        )

        layout.addWidget(
            titulo
        )

        layout.addWidget(
            descripcion
        )