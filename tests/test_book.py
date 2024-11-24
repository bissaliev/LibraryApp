from datetime import date
from unittest import TestCase

from books import Book


class TestBook(TestCase):
    def setUp(self):
        self.data = {
            "id": 1,
            "title": "Преступление и наказание",
            "author": "Федор Достоевский",
            "year": 1866,
            "status": "в наличии",
        }
        self.book_class = Book

    def test_for_creating_book_with_correct_data(self):
        """Класс Book создается с корректными данными."""
        book_obj = self.book_class(**self.data)
        for field, value in self.data.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(book_obj, field), value)

    def test_for_creating_book_with_incorrect_data(self):
        """
        Создание класса Book при некорректных данных вызывает
        исключение ValueError.
        """
        incorrect_data = (
            ("id", "1"),
            ("title", 2024),
            ("author", 2024),
            ("year", date.today().year + 1),
            ("status", "2024"),
        )
        for field, new_value in incorrect_data:
            with self.subTest(field=field):
                old_value = self.data[field]
                self.data[field] = new_value
                with self.assertRaises(ValueError):
                    self.book_class(**self.data)
                self.data[field] = old_value

    def test_of_converting_object_to_dict(self):
        """
        Тест метода `to_dict`, преобразующий объект класса Book в словарь.
        """
        book_obj = self.book_class(**self.data)
        book_to_dict = book_obj.to_dict()
        self.assertEqual(self.data, book_to_dict)

    def test_of_converting_dict_to_obj(self):
        """
        Тест метода класса `from_dict`, преобразующий словарь
        в объект класса Book.
        """
        book_obj = self.book_class(**self.data)
        book_from_dict = self.book_class.from_dict(self.data)
        self.assertEqual(book_obj, book_from_dict)

    def test_of_string_representation(self):
        """Тест строкового представления объекта класса Book."""
        book_obj = self.book_class(**self.data)
        book_string = "\n".join(
            f"{key}: {value}" for key, value in self.data.items()
        )
        self.assertEqual(str(book_obj), book_string)
