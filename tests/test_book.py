from datetime import date
from unittest import TestCase, main

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

    def test_create_book(self):
        """Класс Book создается с корректными данными."""
        book = Book(**self.data)
        for field in self.data:
            with self.subTest(field=field):
                self.assertEqual(getattr(book, field), self.data[field])

    def test_for_creating_book_with_incorrect_data(self):
        """Создание класса Book при некорректных данных вызывает исключение."""
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
                    Book(**self.data)
                self.data[field] = old_value


if __name__ == "__main__":
    main()
