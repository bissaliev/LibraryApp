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
        """Тест: Получение всех книг."""
        books = self.library_manager.get_books()
        self.assertIsInstance(books, list)
        self.assertEqual(len(books), len(self.sample_data))
        first_book = books[0]
        self.assertIsInstance(first_book, Book)
        expected_data = self.sample_data[0]
        for field, expected in expected_data.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(first_book, field), expected)

    def test_get_book_by_id(self):
        """Тест: Получение книги по id."""
        data = self.sample_data[0]
        book = self.library_manager.get_book(data["id"])
        self.assertIsInstance(book, Book)
        for field, expected in data.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(book, field), expected)

    def test_get_book_for_non_existent_id(self):
        """
        Тест: Получение книги по несуществующему id
        возвращает исключение ValueError.
        """
        non_existent_id = 10
        with self.assertRaises(ValueError):
            self.library_manager.get_book(non_existent_id)

    def test_add_book(self):
        """Тест: Добавление книги."""
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

    def test_add_book_with_incorrect_data(self):
        """
        Тест: Добавление книги с некорректными данными
        вызывает исключение ValueError.
        """
        incorrect_data = (
            {"title": 1, "author": "Author", "year": 2000},
            {"title": "New book", "author": 1, "year": 2000},
            {"title": "New book", "author": "Author", "year": "2000"},
        )
        for data in incorrect_data:
            with self.assertRaises(ValueError):
                self.library_manager.add_book(**data)

    def test_add_existent_book(self):
        """
        Тест: Добавление существующей книги вызывает исключение ValueError.
        """
        data = self.sample_data[0]
        title, author, year = data["title"], data["author"], data["year"]
        with self.assertRaises(ValueError):
            self.library_manager.add_book(title, author, year)

    def test_delete_book(self):
        """Тест: Удаление книги по id."""
        all_books = self.library_manager.get_books()
        count_before_deletion = len(all_books)
        first_book_id = all_books[0].id
        deleted_book = self.library_manager.delete_book(first_book_id)
        self.assertIsInstance(deleted_book, Book)
        count_after_deletion = len(self.library_manager.get_books())
        self.assertEqual(count_after_deletion, count_before_deletion - 1)

    def test_delete_book_for_non_existent_id(self):
        """
        Тест: Удаление книги по несуществующему id
        возвращает исключение ValueError.
        """
        non_existent_id = 10
        with self.assertRaises(ValueError):
            self.library_manager.get_book(non_existent_id)

    def test_update_status_of_book(self):
        """Тест: Обновление статуса книги."""
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

    def test_update_status_of_book_with_incorrect_status(self):
        """
        Тест: Обновление статуса книги с некорректным статусом
        вызывает исключение ValueError.
        """
        incorrect_status = "incorrect_status"
        book_to_update = self.library_manager.get_books()[0]
        with self.assertRaises(ValueError):
            self.library_manager.update_book_status(
                book_to_update.id, incorrect_status
            )

    def test_update_status_of_book_for_non_existent_id(self):
        """
        Тест: Обновление книги по несуществующему id
        возвращает исключение ValueError.
        """
        non_existent_id = 10
        with self.assertRaises(ValueError):
            self.library_manager.get_book(non_existent_id)

    def test_search_book(self):
        """Тест: Поиск книг по полям title, author, year."""
        search_fields = self.library_manager.search_fields
        search_data = self.sample_data[0]

        for field in search_fields:
            with self.subTest(field=field):
                search_query = search_data.get(field)
                search_result = self.library_manager.search_book(
                    field, search_query
                )
                self.assertIsInstance(search_result, list)
                self.assertEqual(len(search_result), 1)
                first_book = search_result[0]
                self.assertIsInstance(first_book, Book)
                self.assertEqual(first_book.title, search_data["title"])

    def test_search_invalid_field(self):
        """Тест: Поиск по недопустимому полю выбрасывает исключение."""
        with self.assertRaises(ValueError):
            self.library_manager.search_book("invalid_field", "test")
