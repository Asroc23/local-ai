# ==========================================
# VENTANA DE MEMORIAS
# ==========================================

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QLabel,
    QLineEdit,
    QSpinBox,
    QDialog,
    QFormLayout,
    QDialogButtonBox,
    QMessageBox,
)

from gui.custom_dialog import (
    ConfirmDialog,
    MemoryEditDialog,
)


# ==========================================
# VENTANA PRINCIPAL DE MEMORIAS
# ==========================================

class MemoryWindow(QMainWindow):

    def __init__(self, controller):

        super().__init__()

        self.controller = controller

        self.setWindowTitle(
            "Memorias - Local AI"
        )

        self.resize(
            800,
            600
        )

        self.crear_interfaz()

    # ==========================================
    # CREAR INTERFAZ
    # ==========================================

    def crear_interfaz(self):

        contenedor = QWidget()

        contenedor.setObjectName(
            "contenedor_memorias"
        )

        layout = QVBoxLayout(
            contenedor
        )

        layout.setContentsMargins(
            24,
            22,
            24,
            22
        )

        layout.setSpacing(
            12
        )

        # ==========================================
        # ENCABEZADO
        # ==========================================

        titulo = QLabel(
            "🧠  Memorias permanentes"
        )

        titulo.setObjectName(
            "titulo_memorias"
        )

        descripcion = QLabel(
            "Información que Local AI recuerda para futuras conversaciones."
        )

        descripcion.setObjectName(
            "descripcion_memorias"
        )

        layout.addWidget(
            titulo
        )

        layout.addWidget(
            descripcion
        )

        # ==========================================
        # LISTA
        # ==========================================

        lista = QListWidget()

        lista.setObjectName(
            "lista_memorias"
        )

        lista.setSpacing(
            8
        )

        lista.setSelectionMode(
            QListWidget.SingleSelection
        )

        layout.addWidget(
            lista
        )

        # ==========================================
        # BOTONES
        # ==========================================

        panel_botones = QHBoxLayout()

        panel_botones.setSpacing(
            10
        )

        boton_editar = QPushButton(
            "✏️  Editar memoria"
        )

        boton_editar.setObjectName(
            "boton_editar"
        )

        boton_eliminar = QPushButton(
            "🗑️  Eliminar memoria"
        )

        boton_eliminar.setObjectName(
            "boton_eliminar"
        )

        panel_botones.addWidget(
            boton_editar
        )

        panel_botones.addWidget(
            boton_eliminar
        )

        layout.addLayout(
            panel_botones
        )

        # ==========================================
        # ESTILOS
        # ==========================================

        contenedor.setStyleSheet(
            """
            #contenedor_memorias {
                background-color: #ffffff;
            }

            #titulo_memorias {
                color: #222222;
                font-size: 22px;
                font-weight: 600;
            }

            #descripcion_memorias {
                color: #777777;
                font-size: 14px;
                padding-bottom: 4px;
            }

            #lista_memorias {
                background-color: #f7f7f8;
                border: 1px solid #e2e2e2;
                border-radius: 12px;
                padding: 8px;
                outline: none;
                font-size: 14px;
                color: #333333;
            }

            #lista_memorias::item {
                background-color: #ffffff;
                border: 1px solid #e5e5e5;
                border-radius: 10px;
                padding: 12px;
                margin: 2px 0px;
            }

            #lista_memorias::item:hover {
                background-color: #f5f8ff;
                border: 1px solid #d7e3ff;
            }

            #lista_memorias::item:selected {
                background-color: #eaf1ff;
                color: #1f5fc4;
                border: 1px solid #cbdcff;
            }

            #boton_editar,
            #boton_eliminar {
                min-height: 40px;
                border-radius: 9px;
                padding: 0px 16px;
                font-size: 14px;
                font-weight: 600;
            }

            #boton_editar {
                background-color: #eeeeef;
                color: #333333;
                border: 1px solid #dddddf;
            }

            #boton_editar:hover {
                background-color: #e5e5e7;
            }

            #boton_eliminar {
                background-color: #dc3545;
                color: white;
                border: none;
            }

            #boton_eliminar:hover {
                background-color: #c82333;
            }
            """
        )

        self.setCentralWidget(
            contenedor
        )

        # ==========================================
        # REFERENCIAS
        # ==========================================

        self.lista = lista

        self.boton_editar = boton_editar

        self.boton_eliminar = boton_eliminar

        self.boton_editar.clicked.connect(
            self.editar_memoria
        )

        self.boton_eliminar.clicked.connect(
            self.eliminar_memoria
        )

        self.cargar_memorias()

    # ==========================================
    # CARGAR MEMORIAS
    # ==========================================

    def cargar_memorias(self):

        memorias = self.controller.listar_memorias()

        self.lista.clear()

        for memoria in memorias:

            memory_id = memoria[0]
            category = memoria[1]
            key = memoria[2]
            value = memoria[3]
            importance = memoria[4]

            texto = (
                f"#{memory_id} | "
                f"{category} | "
                f"{key}\n"
                f"{value}\n"
                f"Importancia: {importance}"
            )

            item = QListWidgetItem(
                texto
            )

            item.setData(
                Qt.UserRole,
                memoria
            )

            self.lista.addItem(
                item
            )

    # ==========================================
    # EDITAR MEMORIA
    # ==========================================

    def editar_memoria(self):

        item = self.lista.currentItem()

        if item is None:
            return

        memoria = item.data(Qt.UserRole)

        memory_id = memoria[0]
        category = memoria[1]
        key = memoria[2]
        value = memoria[3]
        importance = memoria[4]

        dialogo = MemoryEditDialog(
            category,
            key,
            value,
            importance
        )

        if dialogo.exec() != QDialog.DialogCode.Accepted:
            return

        self.controller.actualizar_memoria(
            memory_id,
            dialogo.categoria,
            dialogo.clave,
            dialogo.valor,
            dialogo.importancia
        )

        self.cargar_memorias()

    # ==========================================
    # ELIMINAR MEMORIA
    # ==========================================

    def eliminar_memoria(self):

        item = self.lista.currentItem()

        if item is None:
            return

        memoria = item.data(Qt.UserRole)

        memory_id = memoria[0]
        key = memoria[2]
        value = memoria[3]

        dialogo = ConfirmDialog(
            "🗑️ Eliminar memoria",
            "¿Quieres eliminar esta memoria?",
            f"Clave: {key}\n\n{value}\n\nEsta acción no se puede deshacer.",
            texto_confirmar="Eliminar",
            texto_cancelar="Cancelar",
            peligro=True
        )

        if dialogo.exec() != QDialog.DialogCode.Accepted:
            return

        self.controller.eliminar_memoria(
            memory_id
        )

        self.cargar_memorias()