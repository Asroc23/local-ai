# Local AI

Asistente de inteligencia artificial local desarrollado en Python, con LM Studio como motor de lenguaje e interfaz gráfica con PySide6.

## Características

- Integración con LM Studio.
- Respuestas en streaming.
- Interfaz gráfica con PySide6.
- Gestión de conversaciones e historial.
- Base de datos SQLite.
- Memoria permanente y resúmenes.
- Gestión de archivos y documentos.

## Requisitos

- Python 3.12 recomendado.
- Git.
- [LM Studio](https://lmstudio.ai/).
- Un modelo compatible descargado y cargado en LM Studio.

## Instalación en Linux

```bash
git clone https://github.com/Asroc23/local-ai.git
cd local-ai
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
python -m gui.main_window
```
