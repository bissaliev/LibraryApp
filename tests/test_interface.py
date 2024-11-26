from unittest import TestCase
from unittest.mock import MagicMock, patch

from books import Book, Status
from libraries import LibraryManager
from main import (
    add_book,
    delete_book,
    display_book_by_id,
    display_books,
    search_book,
    update_status_of_book,
)


class TestInterface(TestCase):
    """Тестирование интерфейса."""

    def setUp(self):
        self.library = MagicMock(LibraryManager)
        self.data_for_book = {
            "id": 1,
            "title": "Преступление и наказание",
            "author": "Федор Достоевский",
            "year": 1866,
            "status": "выдана",
        }
        self.book = Book(**self.data_for_book)

    @patch("builtins.print")
    def test_display_books(self, mock_print):
        """Тест: Отображение всех книг."""
        books = [self.book]
        self.library.get_books.return_value = books

        display_books(self.library)
        mock_print.assert_called_once_with(
            "\n\n".join(str(book) for book in books)
        )
        self.assertEqual(mock_print.call_count, 1)

    @patch("builtins.print")
    def test_display_books_empty(self, mock_print):
        """Тест: Отображение сообщения, если книг нет."""
        self.library.get_books.return_value = []
        display_books(self.library)
        mock_print.assert_called_once_with("\nВ библиотеке пока нет книг.\n")
        self.assertEqual(mock_print.call_count, 1)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_display_book_by_id(self, mock_print, mock_input):
        """Тест: Успешное отображение книги по ID."""
        mock_input.side_effect = str(self.book.id)
        self.library.get_book.return_value = self.book
        display_book_by_id(self.library)
        self.library.get_book.assert_called_once_with(1)
        mock_print.assert_called_once_with(f"\nНайдена книга:\n{self.book}\n")

    @patch("builtins.input", side_effect=["not number"])
    @patch("builtins.print")
    def test_display_book_by_id_invalid_input(self, mock_print, mock_input):
        """Тест: Обработка некорректного ввода ID книги."""
        display_book_by_id(self.library)
        self.library.get_book.assert_not_called()
        mock_print.assert_called_once_with(
            "\nОшибка: Ввод должен быть числом.\n"
        )

    @patch("builtins.input", side_effect=["100"])
    @patch("builtins.print")
    def test_display_book_by_id_book_not_found(self, mock_print, mock_input):
        """Тест: Обработка отсутствующей книги по ID."""
        msg_error = "Книга с id `100` не найдена."
        self.library.get_book.side_effect = ValueError(msg_error)
        display_book_by_id(self.library)
        self.library.get_book.assert_called_once_with(100)
        mock_print.assert_called_once_with(f"\nОшибка: {msg_error}\n")

    @patch("builtins.input", side_effect=["Title", "Author", "2000"])
    @patch("builtins.print")
    def test_add_existing_book(self, mock_print, mock_input):
        """Тест: Обработка ошибки добавления уже существующей книги."""
        msg_error = "Книга `Title` уже существует."
        self.library.add_book.side_effect = ValueError(msg_error)
        add_book(self.library)
        self.library.add_book.assert_called_once_with("Title", "Author", 2000)
        mock_print.assert_called_once_with(f"\nОшибка: {msg_error}\n")

    @patch("builtins.input", side_effect=["Title", "Author", "not number"])
    @patch("builtins.print")
    def test_add_book_with_invalid_year(self, mock_print, mock_input):
        """Тест: Обработка некорректного ввода года для новой книги."""
        msg_error = "Ввод должен быть числом."
        self.library.add_book.side_effect = ValueError(msg_error)
        add_book(self.library)
        self.library.get_book.assert_not_called()
        mock_print.assert_called_once_with(f"\nОшибка: {msg_error}\n")

    @patch("builtins.input", side_effect=["1"])
    @patch("builtins.print")
    def test_delete_book(self, mock_print, mock_input):
        """Тест: Успешное удаление книги по ID."""
        self.library.delete_book.return_value = self.book
        delete_book(self.library)
        self.library.delete_book.assert_called_once_with(self.book.id)
        mock_print.assert_called_once_with(f"\nКнига удалена:\n{self.book}\n")

    @patch("builtins.input", side_effect=["not number"])
    @patch("builtins.print")
    def test_delete_book_by_id_invalid_input(self, mock_print, mock_input):
        """Тест: Обработка некорректного ввода ID для удаления."""
        delete_book(self.library)
        self.library.delete_book.assert_not_called()
        mock_print.assert_called_once_with(
            "\nОшибка: Ввод должен быть числом.\n"
        )

    @patch("builtins.input", side_effect=["100"])
    @patch("builtins.print")
    def test_delete_non_existing_book(self, mock_print, mock_input):
        """Тест: Обработка удаления несуществующей книги."""
        msg_error = "Книга с id `100` не найдена."
        self.library.delete_book.side_effect = ValueError(msg_error)
        delete_book(self.library)
        self.library.delete_book.assert_called_once_with(100)
        mock_print.assert_called_once_with(f"\nОшибка: {msg_error}\n")

    @patch("builtins.input", side_effect=["1", "2"])
    @patch("builtins.print")
    def test_update_book_status(self, mock_print, mock_input):
        """Тест: Успешное обновление статуса книги."""
        self.library.update_book_status.return_value = self.book
        update_status_of_book(self.library)
        mock_print.assert_any_call(
            "\n".join(f"{i}. {s.value}" for i, s in enumerate(Status, 1))
        )
        self.library.update_book_status.assert_called_once_with(1, "выдана")
        mock_print.assert_any_call(f"\nСтатус книги изменен:\n{self.book}\n")

    @patch("builtins.input", side_effect=["not number"])
    @patch("builtins.print")
    def test_update_status_by_id_invalid_input(self, mock_print, mock_input):
        """Тест: Обработка некорректного ввода ID для обновления статуса."""
        update_status_of_book(self.library)
        self.library.get_book.assert_not_called()
        mock_print.assert_called_once_with(
            "\nОшибка: Ввод должен быть числом.\n"
        )

    @patch("builtins.input", side_effect=["100", "2"])
    @patch("builtins.print")
    def test_update_status_of_non_existing_book(self, mock_print, mock_input):
        """Тест: Обработка обновления статуса несуществующей книги."""
        msg_error = "Книга с id `100` не найдена."
        self.library.update_book_status.side_effect = ValueError(msg_error)
        update_status_of_book(self.library)
        self.library.update_book_status.assert_called_once_with(100, "выдана")
        mock_print.assert_any_call(f"\nОшибка: {msg_error}\n")

    @patch("builtins.input", side_effect=["1", "Test Book"])
    @patch("builtins.print")
    def test_search_book(self, mock_print, mock_input):
        """Тест: Успешный поиск книги по названию."""
        books = [self.book]
        self.library.search_fields = ("title", "author", "year")
        self.library.search_book.return_value = books
        search_book(self.library)
        self.library.search_book.assert_called_once_with("title", "Test Book")
        mock_print.assert_any_call("\n\n".join(str(book) for book in books))

    @patch("builtins.input", side_effect=["4"])
    @patch("builtins.print")
    def test_search_book_with_incorrect_option(self, mock_print, mock_input):
        """Тест: Обработка неверного выбора поля для поиска."""
        search_book(self.library)
        self.library.search_book.assert_not_called()
        mock_print.assert_any_call("\nОшибка: Неверный выбор.\n")
