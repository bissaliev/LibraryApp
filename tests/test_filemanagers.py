import json
from pathlib import Path
from tempfile import NamedTemporaryFile
from unittest import TestCase
from unittest.mock import mock_open, patch

from books import Book, Status
from filemanagers import JsonFileManager
from libraries import LibraryManager


class TestFileManagerSave(TestCase):
    """Тестирование сохранения данных."""

    def setUp(self):
        self.sample_data = [
            {
                "id": 1,
                "title": "Преступление и наказание",
                "author": "Федор Достоевский",
                "year": 1866,
                "status": Status.AVAILABLE.value,
            }
        ]
        with NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
            self.filename = Path(temp_file.name)
        with self.filename.open("w", encoding="utf-8") as file:
            json.dump(self.sample_data, file, ensure_ascii=False, indent=4)
        self.library_manager = LibraryManager(
            Book, JsonFileManager(self.filename)
        )

    def test_save_for_adding_book(self):
        """Тест: Данные сохраняются в файл при добавление."""
        new_data = {
            "title": "1984",
            "author": "Джордж Оруэлл",
            "year": 1949,
        }
        book = self.library_manager.add_book(**new_data)
        with self.filename.open(encoding="utf-8") as file:
            json_file = json.load(file)
            self.assertEqual(len(self.sample_data) + 1, len(json_file))
            self.assertIn(book.to_dict(), json_file)

    def test_save_for_deleting_book(self):
        """Тест: Данные сохраняются в файл при удаление."""
        book = self.library_manager.delete_book(self.sample_data[0]["id"])
        with self.filename.open(encoding="utf-8") as file:
            json_file = json.load(file)
            self.assertEqual(len(self.sample_data) - 1, len(json_file))
            self.assertNotIn(book.to_dict(), json_file)

    def test_save_for_updating_status_of_book(self):
        """Тест: Данные сохраняются в файл при изменение."""
        new_status = Status.BORROWED.value
        self.library_manager.update_book_status(
            self.sample_data[0]["id"], new_status
        )
        with self.filename.open(encoding="utf-8") as file:
            json_file = json.load(file)
            self.assertEqual(len(self.sample_data), len(json_file))
            first_obj = json_file[0]
            self.assertEqual(first_obj["status"], new_status)


class TestFileManagerLoad(TestCase):
    """Тестирование загрузки данных"""

    def test_load(self):
        sample_data = [
            {
                "id": 1,
                "title": "Преступление и наказание",
                "author": "Федор Достоевский",
                "year": 1866,
                "status": Status.AVAILABLE.value,
            }
        ]
        with NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
            self.filename = Path(temp_file.name)
        manager = JsonFileManager(self.filename)
        manager.save(sample_data)
        result = manager.load()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], dict)

    def test_load_file_not_found(self):
        """Тест: исключение FileNotFoundError, если файл не существует."""
        manager = JsonFileManager("non_existent_file.json")
        with (
            patch("pathlib.Path.open", side_effect=FileNotFoundError),
            self.assertRaises(FileNotFoundError),
        ):
            manager.load()

    def test_load_json_decode_error(self):
        """Тест: исключение JSONDecodeError, если файл поврежден."""
        manager = JsonFileManager("corrupted_file.json")

        # Имитируем открытие файла с некорректным содержимым
        invalid_json_content = "{invalid: json}"
        with (
            patch(
                "pathlib.Path.open", mock_open(read_data=invalid_json_content)
            ),
            self.assertRaises(json.JSONDecodeError),
        ):
            manager.load()

    def test_load_empty_file_returns_empty_list(self):
        """Тест: Возвращается пустой список при загрузке пустого файла."""
        with NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
            self.filename = Path(temp_file.name)
        manager = JsonFileManager(self.filename)
        result = manager.load()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
