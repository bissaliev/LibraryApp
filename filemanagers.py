import csv
import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class FileManager(ABC):
    """Абстрактный класс файловый менеджер."""

    def __init__(self, filename: str):
        self.filepath = Path(__file__).parent / filename

    @abstractmethod
    def load(self) -> dict[str, Any]:
        pass

    @abstractmethod
    def save(self, data):
        pass


class JsonFileManager(FileManager):
    """Файловый менеджер для работы с файлом JSON."""

    def load(self) -> list[dict[str, str | int]]:
        """Загрузка данных из файла."""
        try:
            with self.filepath.open(encoding="utf-8") as file:
                first_char = file.read(1)
                if not first_char:
                    return []
                file.seek(0)
                data = json.load(file)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Файл {self.filepath} не найден!") from e
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Ошибка чтения JSON файла {self.filepath}", e.doc, e.pos
            ) from e
        return data

    def save(self, data: list[dict[str, str | int]]) -> None:
        """Сохранение данных в файл."""
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        with self.filepath.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


class CSVFileManager(FileManager):
    """Файловый менеджер для работы с файлом CSV."""

    def __init__(self, filename: str, delimiter: str = ","):
        super().__init__(filename)
        self.delimiter = delimiter

    def load(self) -> list[dict[str, str | int]]:
        """Загрузка данных из файла."""
        if not self.filepath.exists():
            raise FileNotFoundError(f"Файл {self.filepath} не найден.")
        data = []
        with self.filepath.open(encoding="utf-8") as file:
            try:
                csv_reader = csv.DictReader(file, delimiter=self.delimiter)
                for row in csv_reader:
                    for key, value in row.items():
                        if value.isdigit() and key in ("id", "year"):
                            row[key] = int(value)
                    data.append(row)
            except csv.Error as e:
                raise ValueError(f"Ошибка чтения CSV файла: {e}") from e
        return data

    def save(self, data: list[dict[str, str | int]]) -> None:
        """Сохранение данных в файл."""
        fieldnames = list(data[0].keys())
        with self.filepath.open("w", encoding="utf-8") as file:
            csv_writer = csv.DictWriter(
                file, fieldnames=fieldnames, delimiter=self.delimiter
            )
            try:
                csv_writer.writeheader()
                csv_writer.writerows(data)
            except csv.Error as e:
                raise ValueError(f"Ошибка чтения CSV файла: {e}") from e
