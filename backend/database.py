import sqlite3
import os

class DatabaseError(Exception):
    """Error controlado relacionado con la base de datos."""
    pass

class Database:

    def __init__(self, db_path="data/conversations.db"):

        # Crear carpeta data si no existe
        os.makedirs(
            os.path.dirname(db_path),
            exist_ok=True
        )

        self.db_path = db_path

        self.create_tables()

    # ==========================================
    # CONEXIÓN
    # ==========================================

    def connect(self):
        try:
            return sqlite3.connect(self.db_path)

        except sqlite3.Error as e:
            raise DatabaseError(
                f"No se pudo acceder a la base de datos: {e}"
            ) from e

    # ==========================================
    # CREAR TABLAS
    # ==========================================

    def create_tables(self):

        with self.connect() as connection:

            cursor = connection.cursor()

            # ==========================================
            # TABLA DE CONVERSACIONES
            # ==========================================

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    title TEXT NOT NULL,

                    summary TEXT DEFAULT '',

                    summary_message_count INTEGER DEFAULT 0,

                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # ==========================================
            # MIGRACIÓN: AGREGAR SUMMARY
            # ==========================================
            #
            # Esto sirve para bases de datos antiguas
            # que fueron creadas antes de agregar
            # la columna summary.
            #
            # Si summary ya existe, no hace nada.
            #

            cursor.execute("""
                PRAGMA table_info(conversations)
            """)

            columns = [
                row[1]
                for row in cursor.fetchall()
            ]

            if "summary" not in columns:

                cursor.execute("""
                    ALTER TABLE conversations
                    ADD COLUMN summary TEXT DEFAULT ''
                """)

            if "summary_message_count" not in columns:

                cursor.execute("""
                    ALTER TABLE conversations
                    ADD COLUMN summary_message_count INTEGER DEFAULT 0
                """)

            # ==========================================
            # TABLA DE MENSAJES
            # ==========================================

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    conversation_id INTEGER NOT NULL,

                    role TEXT NOT NULL,

                    content TEXT NOT NULL,

                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                    FOREIGN KEY (conversation_id)
                    REFERENCES conversations(id)
                )
            """)

            # ==========================================
            # TABLA DE MEMORIA PERMANENTE
            # ==========================================

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS memory (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    category TEXT NOT NULL,

                    key TEXT NOT NULL,

                    value TEXT NOT NULL,

                    importance INTEGER DEFAULT 3,

                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # ==========================================
            # TABLA DE ARCHIVOS POR CONVERSACIÓN
            # ==========================================

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversation_files (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    conversation_id INTEGER NOT NULL,

                    original_name TEXT NOT NULL,

                    stored_path TEXT NOT NULL,

                    char_count INTEGER DEFAULT 0,

                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                    FOREIGN KEY (conversation_id)
                    REFERENCES conversations(id)
                )
            """)

            # ==========================================
            # MIGRACIÓN: POSICIÓN ORIGINAL DE LOS PDF
            # ==========================================

            cursor.execute("""
                PRAGMA table_info(conversation_files)
            """)

            columnas = [
                columna[1]
                for columna in cursor.fetchall()
            ]

            if "after_message_id" not in columnas:

                cursor.execute("""
                    ALTER TABLE conversation_files
                    ADD COLUMN after_message_id INTEGER
                """)

            connection.commit()


    # ==========================================
    # CREAR CONVERSACIÓN
    # ==========================================

    def create_conversation(self, title="Nueva conversación"):
        try:
            with self.connect() as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO conversations (title) VALUES (?)",
                    (title,)
                )
                connection.commit()
                return cursor.lastrowid

        except sqlite3.Error as e:
            raise DatabaseError(
                f"No se pudo crear la conversación: {e}"
            ) from e

    # ==========================================
    # GUARDAR MENSAJE
    # ==========================================

    def save_message(self, conversation_id, role, content):
        try:
            with self.connect() as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO messages (conversation_id, role, content)
                    VALUES (?, ?, ?)
                """, (conversation_id, role, content))
                connection.commit()

        except sqlite3.Error as e:
            raise DatabaseError(
                f"No se pudo guardar el mensaje: {e}"
            ) from e

    # ==========================================
    # OBTENER MENSAJES
    # ==========================================

    def get_messages(self, conversation_id):
        try:
            with self.connect() as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT role, content
                    FROM messages
                    WHERE conversation_id = ?
                    ORDER BY id ASC
                """, (conversation_id,))
                return cursor.fetchall()

        except sqlite3.Error as e:
            raise DatabaseError(
                f"No se pudieron obtener los mensajes: {e}"
            ) from e

    # ==========================================
    # LISTAR CONVERSACIONES
    # ==========================================

    def get_conversations(self):
        try:
            with self.connect() as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT id, title, created_at
                    FROM conversations
                    ORDER BY id DESC
                """)
                return cursor.fetchall()

        except sqlite3.Error as e:
            raise DatabaseError(
                f"No se pudieron obtener las conversaciones: {e}"
            ) from e

    # ==========================================
    # OBTENER UNA CONVERSACIÓN
    # ==========================================

    def get_conversation(self, conversation_id):
        try:
            with self.connect() as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT id, title, created_at
                    FROM conversations
                    WHERE id = ?
                """, (conversation_id,))
                return cursor.fetchone()

        except sqlite3.Error as e:
            raise DatabaseError(
                f"No se pudo obtener la conversación: {e}"
            ) from e

    # ==========================================
    # OBTENER RESUMEN
    # ==========================================

    def get_summary(self, conversation_id):

        try:

            with self.connect() as connection:

                cursor = connection.cursor()

                cursor.execute("""
                    SELECT summary
                    FROM conversations
                    WHERE id = ?
                """, (conversation_id,))

                result = cursor.fetchone()

                if not result:
                    return ""

                return result[0] or ""

        except sqlite3.Error as e:

            raise DatabaseError(
                f"No se pudo obtener el resumen: {e}"
            ) from e

    # ==========================================
    # GUARDAR RESUMEN
    # ==========================================

    def save_summary(self, conversation_id, summary):

        try:

            with self.connect() as connection:

                cursor = connection.cursor()

                cursor.execute("""
                    UPDATE conversations
                    SET summary = ?
                    WHERE id = ?
                """, (summary, conversation_id))

                connection.commit()

        except sqlite3.Error as e:

            raise DatabaseError(
                f"No se pudo guardar el resumen: {e}"
            ) from e

    # ==========================================
    # OBTENER CANTIDAD DE MENSAJES DEL RESUMEN
    # ==========================================

    def get_summary_message_count(self, conversation_id):

        try:

            with self.connect() as connection:

                cursor = connection.cursor()

                cursor.execute("""
                    SELECT summary_message_count
                    FROM conversations
                    WHERE id = ?
                """, (conversation_id,))

                result = cursor.fetchone()

                if not result:
                    return 0

                return result[0] or 0

        except sqlite3.Error as e:

            raise DatabaseError(
                f"No se pudo obtener el contador del resumen: {e}"
            ) from e

    # ==========================================
    # GUARDAR CANTIDAD DE MENSAJES DEL RESUMEN
    # ==========================================

    def save_summary_message_count(self, conversation_id, message_count):

        try:

            with self.connect() as connection:

                cursor = connection.cursor()

                cursor.execute("""
                    UPDATE conversations
                    SET summary_message_count = ?
                    WHERE id = ?
                """, (message_count, conversation_id))

                connection.commit()

        except sqlite3.Error as e:

            raise DatabaseError(
                f"No se pudo guardar el contador del resumen: {e}"
            ) from e

    # ==========================================
    # CAMBIAR TÍTULO
    # ==========================================

    def update_conversation_title(self, conversation_id, title):

        try:

            with self.connect() as connection:

                cursor = connection.cursor()

                cursor.execute("""
                    UPDATE conversations
                    SET title = ?
                    WHERE id = ?
                """, (title, conversation_id))

                connection.commit()

        except sqlite3.Error as e:

            raise DatabaseError(
                f"No se pudo actualizar el título: {e}"
            ) from e

    # ==========================================
    # ELIMINAR CONVERSACIÓN
    # ==========================================

    def delete_conversation(self, conversation_id):

        try:

            with self.connect() as connection:

                cursor = connection.cursor()

                cursor.execute("""
                    DELETE FROM messages
                    WHERE conversation_id = ?
                """, (conversation_id,))

                cursor.execute("""
                    DELETE FROM conversations
                    WHERE id = ?
                """, (conversation_id,))

                connection.commit()

        except sqlite3.Error as e:

            raise DatabaseError(
                f"No se pudo eliminar la conversación: {e}"
            ) from e

    # ==========================================
    # GUARDAR MEMORIA PERMANENTE
    # ==========================================

    def save_memory(self, category, key, value, importance=3):

        try:

            with self.connect() as connection:

                cursor = connection.cursor()

                cursor.execute("""
                    INSERT INTO memory (category, key, value, importance)
                    VALUES (?, ?, ?, ?)
                """, (category, key, value, importance))

                connection.commit()

                return cursor.lastrowid

        except sqlite3.Error as e:

            raise DatabaseError(
                f"No se pudo guardar la memoria: {e}"
            ) from e
    # ==========================================
    # OBTENER TODAS LAS MEMORIAS
    # ==========================================

    def get_memories(self):

        try:

            with self.connect() as connection:

                cursor = connection.cursor()

                cursor.execute("""
                    SELECT id, category, key, value, importance, created_at, updated_at
                    FROM memory
                    ORDER BY importance DESC, id ASC
                """)

                return cursor.fetchall()

        except sqlite3.Error as e:

            raise DatabaseError(
                f"No se pudieron obtener las memorias: {e}"
            ) from e

    # ==========================================
    # OBTENER UNA MEMORIA
    # ==========================================

    def get_memory(self, memory_id):

        try:

            with self.connect() as connection:

                cursor = connection.cursor()

                cursor.execute("""
                    SELECT id, category, key, value, importance, created_at, updated_at
                    FROM memory
                    WHERE id = ?
                """, (memory_id,))

                return cursor.fetchone()

        except sqlite3.Error as e:

            raise DatabaseError(
                f"No se pudo obtener la memoria: {e}"
            ) from e

    # ==========================================
    # BUSCAR MEMORIA POR CATEGORÍA Y CLAVE
    # ==========================================

    def get_memory_by_key(self, category, key):

        try:

            with self.connect() as connection:

                cursor = connection.cursor()

                cursor.execute("""
                    SELECT id, category, key, value, importance, created_at, updated_at
                    FROM memory
                    WHERE category = ? AND key = ?
                    ORDER BY id DESC
                    LIMIT 1
                """, (category, key))

                return cursor.fetchone()

        except sqlite3.Error as e:

            raise DatabaseError(
                f"No se pudo buscar la memoria: {e}"
            ) from e

    # ==========================================
    # ACTUALIZAR MEMORIA
    # ==========================================

    def update_memory(self, memory_id, category, key, value, importance):

        try:

            with self.connect() as connection:

                cursor = connection.cursor()

                cursor.execute("""
                    UPDATE memory
                    SET category = ?, key = ?, value = ?, importance = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (category, key, value, importance, memory_id))

                connection.commit()

                return cursor.rowcount

        except sqlite3.Error as e:

            raise DatabaseError(
                f"No se pudo actualizar la memoria: {e}"
            ) from e

    # ==========================================
    # ELIMINAR MEMORIA
    # ==========================================

    def delete_memory(self, memory_id):

        try:

            with self.connect() as connection:

                cursor = connection.cursor()

                cursor.execute("""
                    DELETE FROM memory
                    WHERE id = ?
                """, (memory_id,))

                connection.commit()

                return cursor.rowcount

        except sqlite3.Error as e:

            raise DatabaseError(
                f"No se pudo eliminar la memoria: {e}"
            ) from e

    # ==========================================
    # REGISTRAR ARCHIVO DE CONVERSACIÓN
    # ==========================================

    def save_conversation_file(
        self,
        conversation_id,
        original_name,
        stored_path,
        char_count=0,
        after_message_id=None
    ):
        try:
            with self.connect() as connection:
                cursor = connection.cursor()

                cursor.execute("""
                    INSERT INTO conversation_files (
                        conversation_id,
                        original_name,
                        stored_path,
                        char_count,
                        after_message_id
                    )
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    conversation_id,
                    original_name,
                    stored_path,
                    char_count,
                    after_message_id
                ))

                connection.commit()
                return cursor.lastrowid

        except sqlite3.Error as e:
            raise DatabaseError(
                f"No se pudo registrar el archivo: {e}"
            ) from e

    # ==========================================
    # OBTENER ARCHIVOS DE UNA CONVERSACIÓN
    # ==========================================

    def get_conversation_files(self, conversation_id):

        try:
            with self.connect() as connection:

                cursor = connection.cursor()

                cursor.execute("""
                    SELECT
                        id,
                        conversation_id,
                        original_name,
                        stored_path,
                        char_count,
                        created_at,
                        after_message_id
                    FROM conversation_files
                    WHERE conversation_id = ?
                    ORDER BY id ASC
                """, (conversation_id,))

                return cursor.fetchall()

        except sqlite3.Error as e:
            raise DatabaseError(
                f"No se pudieron obtener los archivos: {e}"
            ) from e