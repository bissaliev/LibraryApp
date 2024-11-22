import json
from pathlib import Path
from tempfile import NamedTemporaryFile
from unittest import TestCase

from books import Book, Status
from filemanagers import JsonFileManager
from libraries import LibraryManager


class TestLibraryManager(TestCase):
    """Тестовый класс для тестирования класса LibraryManager."""

    def setUp(self):
        # данные для тестирования
        self.sample_data = [
            {
                "id": 1,
                "title": "Преступление и наказание",
                "author": "Федор Достоевский",
                "year": 1866,
            },
            {
                "id": 2,
                "title": "1984",
                "author": "Джордж Оруэлл",
                "year": 1949,
            },
        ]
        # Создаем временный файл для хранения книг
        with NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
            # Сохраняем путь до файла
            self.file_path = Path(temp_file.name)
        # Записываем данные в файл
        with self.file_path.open("w", encoding="utf-8") as json_file:
            json.dump(
                self.sample_data, json_file, ensure_ascii=False, indent=4
            )
        self.library_manager = LibraryManager(
            Book, JsonFileManager(self.file_path)
        )

    def tearDown(self):
        """Удаляем временный файл."""
        self.file_path.unlink(missing_ok=True)

    def test_get_books(self):
        """Тест получения всех книг."""
        books = self.library_manager.get_books()
        self.assertIsInstance(books, list)
        self.assertEqual(len(books), len(self.sample_data))
        first_book = books[0]
        self.assertIsInstance(first_book, Book)
        data = self.sample_data[0]
        for key, value in data.items():
            with self.subTest(field=key):
                self.assertEqual(getattr(first_book, key), value)

    def test_get_book_by_id(self):
        """Тест получения книги по id."""
        data = self.sample_data[0]
        book = self.library_manager.get_book(data["id"])
        self.assertIsInstance(book, Book)
        for key, value in data.items():
            with self.subTest(field=key):
                self.assertEqual(getattr(book, key), value)

    def test_add_book(self):
        """Тест добавления книги."""
        new_data = {
            "title": "New book",
            "author": "Author",
            "year": 2000,
        }
        all_books = self.library_manager.get_books()
        count_before_adding = len(all_books)
        added_book = self.library_manager.add_book(**new_data)
        self.assertIsInstance(added_book, Book)
        self.assertTrue(added_book.id)
        self.assertIsInstance(added_book.id, int)
        all_books = self.library_manager.get_books()
        count_after_adding = len(all_books)
        self.assertEqual(count_after_adding, count_before_adding + 1)
        self.assertIn(added_book, all_books)

    def test_delete_book(self):
        """Тест удаления книги по id."""
        all_books = self.library_manager.get_books()
        count_before_deletion = len(all_books)
        first_book_id = all_books[0].id
        deleted_book = self.library_manager.delete_book(first_book_id)
        self.assertIsInstance(deleted_book, Book)
        count_after_deletion = len(self.library_manager.get_books())
        self.assertEqual(count_after_deletion, count_before_deletion - 1)

    def test_update_status_of_book(self):
        """Тест обновления статуса книги."""
        book_before_update = self.library_manager.get_books()[0]
        status_before_update = book_before_update.status
        updated_book = self.library_manager.update_book_status(
            book_before_update.id, Status.BORROWED.value
        )
        self.assertIsInstance(updated_book, Book)
        book_after_update = self.library_manager.get_book(
            book_before_update.id
        )
        self.assertNotEqual(status_before_update, book_after_update.status)
        self.assertEqual(book_after_update.status, Status.BORROWED.value)

    def test_search_book(self):
        """Тест поиска книг по полям title, author, year."""
        search_fields = ("title", "author", "year")
        search_data = self.sample_data[0]
        search_parameters = (
            search_data["title"],
            search_data["author"],
            search_data["year"],
        )
        for field, param in zip(search_fields, search_parameters):
            with self.subTest(field=field):
                search_result = self.library_manager.search_book(field, param)
                self.assertIsInstance(search_result, list)
                self.assertEqual(len(search_result), 1)
                first_book = search_result[0]
                self.assertEqual(first_book.title, search_data["title"])
