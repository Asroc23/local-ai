import os
import json
import httpx

from dotenv import load_dotenv


# ==========================================================
# ERROR CONTROLADO DE LM STUDIO
# ==========================================================

class LMStudioError(Exception):
    """Error controlado relacionado con LM Studio."""
    pass


# ==========================================================
# CARGAR VARIABLES DEL ARCHIVO .env
# ==========================================================

load_dotenv()


class LMStudioClient:

    def __init__(self):

        # --------------------------------------------------
        # Configuración del servidor LM Studio
        # --------------------------------------------------

        host = os.getenv(
            "LM_STUDIO_HOST",
            "127.0.0.1"
        )

        port = os.getenv(
            "LM_STUDIO_PORT",
            "1234"
        )

        # --------------------------------------------------
        # Modelo
        # --------------------------------------------------

        self.model = os.getenv(
            "LM_STUDIO_MODEL",
            "google/gemma-3-4b"
        )

        # --------------------------------------------------
        # URL base
        # --------------------------------------------------

        self.base_url = f"http://{host}:{port}/v1"

        # --------------------------------------------------
        # Estadísticas de la última respuesta
        # --------------------------------------------------

        self.last_usage = None

    # ======================================================
    # OBTENER MODELOS
    # ======================================================

    async def get_models(self):
        """
        Obtiene los modelos disponibles en LM Studio.
        """

        url = f"{self.base_url}/models"

        try:

            async with httpx.AsyncClient() as client:

                response = await client.get(
                    url,
                    timeout=None
                )

                response.raise_for_status()

                return response.json()

        except httpx.ConnectError as e:

            raise LMStudioError(
                "No se pudo conectar con LM Studio. "
                "Verifica que el servidor esté ejecutándose."
            ) from e

        except httpx.HTTPStatusError as e:

            raise LMStudioError(
                f"LM Studio respondió con un error HTTP "
                f"({e.response.status_code})."
            ) from e

        except httpx.RequestError as e:

            raise LMStudioError(
                f"Error de comunicación con LM Studio: {e}"
            ) from e

    # ======================================================
    # CHAT NORMAL
    # ======================================================

    async def chat(
        self,
        messages,
        temperature=0.7
    ):
        """
        Envía una conversación a LM Studio
        y devuelve la respuesta completa.
        """

        url = f"{self.base_url}/chat/completions"

        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature
        }

        try:

            async with httpx.AsyncClient() as client:

                response = await client.post(
                    url,
                    json=data,
                    timeout=None
                )

                response.raise_for_status()

                result = response.json()

                # --------------------------------------------------
                # Guardar estadísticas
                # --------------------------------------------------

                self.last_usage = result.get("usage")

                # --------------------------------------------------
                # Obtener respuesta
                # --------------------------------------------------

                choices = result.get("choices", [])

                if not choices:
                    return ""

                message = choices[0].get(
                    "message",
                    {}
                )

                return message.get(
                    "content",
                    ""
                )

        except httpx.ConnectError as e:

            raise LMStudioError(
                "No se pudo conectar con LM Studio. "
                "Verifica que el servidor esté ejecutándose."
            ) from e

        except httpx.HTTPStatusError as e:

            raise LMStudioError(
                f"LM Studio respondió con un error HTTP "
                f"({e.response.status_code})."
            ) from e

        except httpx.RequestError as e:

            raise LMStudioError(
                f"Error de comunicación con LM Studio: {e}"
            ) from e

    # ======================================================
    # CHAT CON STREAMING
    # ======================================================

    async def chat_stream(
        self,
        messages,
        temperature=0.7
    ):
        """
        Envía una conversación a LM Studio utilizando
        streaming.

        Va devolviendo fragmentos de texto conforme
        el modelo los genera.

        Al finalizar, guarda las estadísticas de uso
        proporcionadas por LM Studio.
        """

        url = f"{self.base_url}/chat/completions"

        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": True,
            "stream_options": {
                "include_usage": True
            }
        }

        # --------------------------------------------------
        # Reiniciar estadísticas
        # --------------------------------------------------

        self.last_usage = None

        try:

            # --------------------------------------------------
            # Conexión con LM Studio
            # --------------------------------------------------

            async with httpx.AsyncClient() as client:

                async with client.stream(
                    "POST",
                    url,
                    json=data,
                    timeout=None
                ) as response:

                    # --------------------------------------------------
                    # Verificar respuesta HTTP
                    # --------------------------------------------------

                    response.raise_for_status()

                    # --------------------------------------------------
                    # Leer streaming
                    # --------------------------------------------------

                    async for line in response.aiter_lines():

                        # Ignorar líneas vacías
                        if not line:
                            continue

                        # LM Studio utiliza Server-Sent Events
                        if not line.startswith("data: "):
                            continue

                        # Eliminar "data: "
                        data_line = line[6:]

                        # --------------------------------------------------
                        # Fin del streaming
                        # --------------------------------------------------

                        if data_line == "[DONE]":
                            break

                        # --------------------------------------------------
                        # Convertir JSON
                        # --------------------------------------------------

                        try:

                            chunk = json.loads(
                                data_line
                            )

                        except json.JSONDecodeError:

                            continue

                        # --------------------------------------------------
                        # Obtener estadísticas
                        # --------------------------------------------------

                        usage = chunk.get(
                            "usage"
                        )

                        if usage:

                            self.last_usage = usage

                        # --------------------------------------------------
                        # Obtener choices
                        # --------------------------------------------------

                        choices = chunk.get(
                            "choices",
                            []
                        )

                        if not choices:
                            continue

                        # --------------------------------------------------
                        # Obtener delta
                        # --------------------------------------------------

                        delta = choices[0].get(
                            "delta",
                            {}
                        )

                        # --------------------------------------------------
                        # Obtener contenido
                        # --------------------------------------------------

                        content = delta.get(
                            "content"
                        )

                        if content:

                            yield content

        except httpx.ConnectError as e:

            raise LMStudioError(
                "No se pudo conectar con LM Studio. "
                "Verifica que el servidor esté ejecutándose."
            ) from e

        except httpx.HTTPStatusError as e:

            raise LMStudioError(
                f"LM Studio respondió con un error HTTP "
                f"({e.response.status_code})."
            ) from e

        except httpx.RequestError as e:

            raise LMStudioError(
                f"Error de comunicación con LM Studio: {e}"
            ) from e