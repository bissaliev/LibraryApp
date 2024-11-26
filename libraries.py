from books import Book
from filemanagers import FileManager


class LibraryManager:
    search_fields: tuple[str] = ("title", "author", "year")

    def __init__(self, book_class: type[Book], file_manager: FileManager):
        self.file_manager = file_manager
        self.book_class: type[Book] = book_class
        self._books: dict[int, Book] = {}
        self._next_id: int = 1
        self._initialize_books()

    def _initialize_books(self) -> None:
        """Загружает книги из файла и определяет следующий доступный ID."""
        data = self.file_manager.load()
        if data:
            self._books = {
                item["id"]: self.book_class.from_dict(item) for item in data
            }
            self._next_id = max(int(id) for id in self._books) + 1

    def _save_books(self) -> None:
        """Сохраняет текущие данные о книгах в файл."""
        data = [book.to_dict() for book in self._books.values()]
        self.file_manager.save(data)

    def get_book(self, id: int) -> Book:
        """Возвращает книгу по её ID."""
        book = self._books.get(id)
        if not book:
            raise ValueError(f"Книга с id `{id}` не найдена.")
        return book

    def get_books(self) -> list[Book]:
        """Возвращает список всех книг."""
        return [book for book in self._books.values()]

    def add_book(self, title: str, author: str, year: int) -> Book:
        """Добавляет новую книгу в библиотеку."""
        # TODO: Проверка что нового id нет в библиотеке
        # TODO: Проверка на равенство
        try:
            new_book = self.book_class(
                id=self._next_id,
                title=title,
                author=author,
                year=year,
            )
        except ValueError as error:
            raise ValueError(str(error)) from error
        for book in self._books.values():
            if book == new_book:
                raise ValueError(f"Книга `{new_book.title}` уже существует.")
        self._books[new_book.id] = new_book
        self._save_books()
        self._next_id += 1
        return new_book

    def delete_book(self, id: int) -> Book:
        """Удаляет книгу по ID."""
        deleted_book = self._books.pop(id)
        if not deleted_book:
            raise ValueError(f"Книга с id `{id}` не найдена.")
        self._save_books()
        return deleted_book

    def update_book_status(self, id: int, new_status: str) -> Book:
        """Обновляет статус книги."""
        updated_book = self._books.get(id)
        if not updated_book:
            raise ValueError(f"Книга с id `{id}` не найдена.")
        updated_book.status = new_status
        self._save_books()
        return updated_book

    def search_book(self, field_name: str, query: str | int) -> list[Book]:
        """Поиск книг по полям title, author, year."""
        field_name = field_name.strip().lower()
        if field_name not in self.search_fields:
            raise ValueError(f"Поиск книг по полю {field_name} не доступен.")
        if isinstance(query, str):
            query = query.strip().lower()
        output = []
        for book in self._books.values():
            field_value = getattr(book, field_name)
            if self._matches_field(field_value, query):
                output.append(book)
        return output

    @staticmethod
    def _matches_field(field_value: str | int, query: str | int) -> bool:
        """Проверка соответствия значения полю запроса."""
        if isinstance(field_value, str) and isinstance(query, str):
            return query in field_value.lower()
        elif isinstance(field_value, int) and isinstance(query, int):
            return query == field_value
        return False
