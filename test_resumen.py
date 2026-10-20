import asyncio

from backend.database import Database
from backend.memory import Memory
from backend.lmstudio import LMStudioClient


SYSTEM_MESSAGE = {
    "role": "system",
    "content": (
        "Eres un asistente de inteligencia artificial "
        "útil, claro y preciso. "
        "Mantén el contexto de la conversación."
    )
}


async def main():

    db = Database()
    client = LMStudioClient()

    memory = Memory(
        db,
        SYSTEM_MESSAGE,
        client
    )

    # Crear conversación de prueba
    conversation_id = db.create_conversation(
        "Prueba de correcciones"
    )

    print()
    print("=" * 50)
    print("🧪 PRUEBA DE CORRECCIONES EN RESUMEN")
    print("=" * 50)
    print(f"📂 Conversación creada: #{conversation_id}")

    mensajes = [
        # ==========================================
        # PRIMEROS 20 MENSAJES
        # ESTOS SERÁN RESUMIDOS
        # ==========================================

        ("user", "Mi nombre es Oscar."),
        ("assistant", "Mucho gusto, Oscar."),

        ("user", "Estoy desarrollando un proyecto llamado Alfa."),
        ("assistant", "Entendido, tu proyecto se llama Alfa."),

        ("user", "El proyecto está desarrollado en Python."),
        ("assistant", "Perfecto, utilizarás Python."),

        ("user", "También utilizo SQLite para guardar datos."),
        ("assistant", "SQLite se utilizará para almacenar los datos."),

        ("user", "El proyecto funciona en Linux."),
        ("assistant", "Entendido, el proyecto funciona en Linux."),

        ("user", "Estoy utilizando LM Studio."),
        ("assistant", "LM Studio forma parte del proyecto."),

        ("user", "Quiero que el proyecto tenga memoria."),
        ("assistant", "La memoria será una característica importante."),

        ("user", "Quiero que tenga conversaciones."),
        ("assistant", "Las conversaciones también forman parte del proyecto."),

        ("user", "Corrección importante: el nombre Alfa era incorrecto."),
        ("assistant", "Entendido, el nombre anterior era incorrecto."),

        # ==========================================
        # MENSAJE 19 Y 20
        # CORRECCIÓN DEFINITIVA
        # ==========================================

        ("user", "El nombre correcto del proyecto es Shippo."),
        ("assistant", "Entendido. El proyecto se llama Shippo."),

        # ==========================================
        # ÚLTIMOS 20 MENSAJES
        # NO SE RESUMEN
        # ==========================================

        ("user", "Quiero que el sistema sea modular."),
        ("assistant", "Entendido."),

        ("user", "Quiero separar el backend."),
        ("assistant", "De acuerdo."),

        ("user", "También quiero mejorar el manejo de errores."),
        ("assistant", "Es una buena consideración."),

        ("user", "Quiero controlar mejor el contexto."),
        ("assistant", "Entendido."),

        ("user", "También quiero poder cambiar de modelo."),
        ("assistant", "Eso permitirá mayor flexibilidad."),

        ("user", "Quiero agregar una interfaz gráfica."),
        ("assistant", "La interfaz gráfica puede añadirse posteriormente."),

        ("user", "Quiero mantener SQLite."),
        ("assistant", "SQLite continuará almacenando las conversaciones."),

        ("user", "Quiero que el sistema sea fácil de ampliar."),
        ("assistant", "Entendido."),

        ("user", "Quiero agregar más funciones en el futuro."),
        ("assistant", "Perfecto."),

        ("user", "Esta es una prueba del sistema de memoria."),
        ("assistant", "Prueba recibida.")
    ]

    print(f"💾 Mensajes preparados: {len(mensajes)}")

    # Guardar mensajes
    for role, content in mensajes:
        db.save_message(
            conversation_id,
            role,
            content
        )

    # Cargar memoria
    messages = memory.cargar_memoria(
        conversation_id
    )

    # Generar resumen
    await memory.generar_resumen(
        conversation_id,
        messages
    )

    # Leer resumen generado
    resumen = db.get_summary(
        conversation_id
    )

    contador = db.get_summary_message_count(
        conversation_id
    )

    print()
    print("=" * 50)
    print("🧠 RESUMEN GENERADO")
    print("=" * 50)
    print(resumen)

    print()
    print("=" * 50)
    print("📊 DATOS DEL RESUMEN")
    print("=" * 50)

    print(f"Mensajes totales: {len(mensajes)}")
    print(f"Mensajes registrados para resumen: {contador}")
    print(f"Longitud del resumen: {len(resumen)} caracteres")

    print()
    print("=" * 50)
    print("🔎 COMPROBACIÓN DE CORRECCIÓN")
    print("=" * 50)

    if "Shippo" in resumen:
        print("✅ Shippo aparece en el resumen.")
    else:
        print("❌ Shippo NO aparece en el resumen.")

    if "Alfa" in resumen:
        print("⚠️ Alfa todavía aparece en el resumen.")
    else:
        print("✅ Alfa fue descartado correctamente.")

    print()
    print(f"🗑️ Puedes eliminar después la conversación #{conversation_id}.")


if __name__ == "__main__":
    asyncio.run(main())