import json

from books import Book


class LibraryManager:
    def __init__(self, book: Book, filename: str = "library.json"):
        self.filename: str = filename
        self.book = book
        self.books: dict[str, Book] = {}
        self.load_book()

    def load_book(self):
        try:
            with open(self.filename, encoding="utf-8") as file:
                data = json.load(file)
                self.books = {
                    key: self.book.from_dict(value)
                    for key, value in data.items()
                }
        except FileNotFoundError:
            print(f"Файла `{self.filename}` не существует.")

    def save_books(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            data = {book.title: book.to_dict() for book in self.books.values()}
            json.dump(data, file, ensure_ascii=False, indent=4)

    def get_book(self, id: int):
        return self._binary_search(list(self.books.values()), id)

    def get_books(self):
        yield from self.books.values()

    def add_book(self, title: str, author: str, year: int):
        book = Book(title=title, author=author, year=year)
        if book.title in self.books and book == self.books[book.title]:
            print(f"Книга `{book.title}` уже существует.")
            return
        next_id = max(book.id for book in self.books.values()) + 1
        book.id = next_id
        self.books[book.id] = book
        self.save_books()
        return book

    def delete_book(self, id: int):
        try:
            current_book = self.books[id]
        except KeyError:
            print(f"Книги с id `{id}` не существует.")
        else:
            del self.books[id]
            self.save_books()
            print(f"Книга `{current_book.title}` удалена.")

    def update_book_status(self, id: int, status: str):
        try:
            current_book = self.books[id]
        except KeyError:
            print(f"Книга `{current_book.title}` удалена.")
        else:
            current_book.status = status
            self.save_books()
            print(
                f"Статус книги `{current_book.title}` изменён на `{status}`."
            )

    def search_book(self, field: str, query: str):
        """Поиск книг по полям title, author, year."""
        field = field.lower()
        return getattr(self, f"_get_book_by_{field}")(query)

    def _binary_search(self, objs: list[Book], id: int):
        if objs[0].id > id or objs[-1].id < id:
            return None
        left = 0
        right = len(objs)
        while left < right:
            middle = (left + right) // 2
            obj = objs[middle]
            if id > obj.id:
                left = middle + 1
            elif id < obj.id:
                right = middle
            else:
                return obj
        return objs[left] if objs[left].id == id else None

    def _get_book_by_author(self, author: str):
        output = []
        for book in self.books.values():
            if book.author == author:
                output.append(book)
        return output

    def _get_book_by_title(self, title: str):
        return [self.books.get(title)]

    def _get_book_by_year(self, year: str):
        output = []
        for book in self.books.values():
            if book.year == year:
                output.append(book)
        return output
