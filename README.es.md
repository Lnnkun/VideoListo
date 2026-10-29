[中文](README.md) | [English](README.en.md) | **Español**

# VideoListo V1.0

Genera automáticamente subtítulos (`.srt`), título, descripción, capítulos con marcas de tiempo y etiquetas para vídeos en español.

## Requisitos previos

- Python y [ffmpeg](https://ffmpeg.org/) (Whisper lo necesita para leer los vídeos)
- Una cuenta de [OpenRouter](https://openrouter.ai/) y su clave de API

## Instalación

```powershell
git clone https://github.com/Lnnkun/VideoListo.git
cd VideoListo
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Edita `.env` y pon tu propia `OPENROUTER_API_KEY`.

> La línea de `torch` en `requirements.txt` es la versión CUDA (`+cu128`). Si no tienes una GPU NVIDIA, cámbiala primero por `torch` a secas.

## Uso

```powershell
python main.py video.mp4
```

Genera `video.srt` (subtítulos) y `video_meta.md` (títulos, descripción, capítulos, etiquetas), e imprime el coste de la IA en esa ejecución.

## Rendimiento

Probado en una RTX 4060 (8 GB) con el modelo Whisper small.

La transcripción por lotes de 19 vídeos explicativos en español (de 4 a 50 minutos cada uno, unos 336 minutos de audio en total) tardó unos 20 minutos, es decir, unas **16,6 veces la velocidad real** (un vídeo de 10 minutos en unos 36 segundos). Los tiempos incluyen la carga del modelo en cada ejecución.

## Coste

Datos provisionales (Video_1, unos 4 minutos): unos 0,0018 US$; unos 0,0045 US$ para un vídeo de 10 minutos. Se sustituirán tras el Video 4.

## Capturas de pantalla

Por añadir.
