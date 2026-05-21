from pathlib import Path
from faster_whisper import WhisperModel


MODEL_SIZE = "base"

model = WhisperModel(
    MODEL_SIZE,
    device="cpu",
    compute_type="int8"
)


def transcribe_audio(file_path: str) -> str:
    """
    Распознаёт речь из аудиофайла и возвращает текст.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    segments, info = model.transcribe(
        str(path),
        language="ru",
        beam_size=5
    )

    text_parts = []

    for segment in segments:
        text_parts.append(segment.text.strip())

    recognized_text = " ".join(text_parts).strip()

    return recognized_text