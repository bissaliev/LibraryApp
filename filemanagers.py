import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class FileManager(ABC):
    @abstractmethod
    def load(self) -> dict[str, Any]:
        pass

    @abstractmethod
    def save(self, data):
        pass


class JsonFileManager(FileManager):
    def __init__(self, filename: str):
        self.filepath = Path(__file__).parent / filename

    def load(self) -> list[dict[str, str | int]]:
        try:
            with self.filepath.open(encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Файл {self.filepath} не найден!") from e
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Ошибка чтения JSON файла {self.filepath}", e.doc, e.pos
            ) from e
        return data

    def save(self, data: list[dict[str, str | int]]) -> None:
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        with self.filepath.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
