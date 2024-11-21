import json


class Book:
    def __init__(
        self,
        title: str,
        author: str,
        year: int,
        id: int = None,
        status: str = "в наличии",
    ):
        self.id: int = id
        self.title: str = title
        self.author: str = author
        self.year: int = year
        self.status: str = status

    def __str__(self):
        return str(self.to_dict())

    def __repr__(self):
        return f"{self.__class__.__name__}({self.title})"

    def to_dict(self):
        """Преобразование объекта книги в словарь."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data):
        """Создание объекта книги из словаря."""
        return cls(**data)

    def __eq__(self, other: "Book"):
        return (self.title, self.author, self.year) == (
            other.title,
            other.author,
            other.year,
        )


class LibraryManager:
    def __init__(self, filename: str = "library.json"):
        self.filename: str = filename
        self.books: dict[str, Book] = {}
        self.load_book()

    def load_book(self):
        try:
            with open(self.filename, encoding="utf-8") as file:
                data = json.load(file)
                self.books = {
                    key: Book(**value) for key, value in data.items()
                }
        except FileNotFoundError:
            print(f"Файла `{self.filename}` не существует.")

    def save_books(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            data = {book.title: book.to_dict() for book in self.books.values()}
            json.dump(data, file, ensure_ascii=False, indent=4)

    def get_book(self, id):
        return self.books.get(str(id))

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

    def _binary_search(objs: list[Book], id):
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
        return objs[left] if objs[left].id == id else []

    def _get_book_by_id(self, id: int):
        return self._binary_search(list(self.books.values()), id)

    def _get_book_by_author(self, author: str):
        output = []
        for book in self.books.values():
            if book.author == author:
                output.append(book)
        return output

    def _get_book_by_title(self, title: str):
        return [self.books.get(title)]


if __name__ == "__main__":
    library = LibraryManager()
    for book in library.get_books():
        print(book)
    print(library.search_book("author", "Джоан Роулинг"))
    library.add_book("Гарри Поттер и Дары Смерти", "Джоан Роулинг", 2007)
    print(library.search_book("author", "Джоан Роулинг"))
