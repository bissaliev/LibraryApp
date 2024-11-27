from dataclasses import asdict, dataclass, field
from datetime import date
from enum import Enum


class Status(Enum):
    """Статусы книг."""

    AVAILABLE: str = "в наличии"
    BORROWED: str = "выдана"


@dataclass
class Book:
    """Класс книг."""

    id: int = field(compare=False)
    title: str
    author: str
    year: int
    status: str = field(compare=False, default=Status.AVAILABLE.value)

    def __post_init__(self):
        # Валидация id
        if not isinstance(self.id, int) or self.id < 1:
            raise ValueError(
                "ID книги должно быть целым положительным числом."
            )

        # Валидация title
        self.title = self.validate_non_empty_string("title", self.title)

        # Валидация author
        self.author = self.validate_non_empty_string("author", self.author)

        # Валидация year
        if not isinstance(self.year, int) or self.year > date.today().year:
            raise ValueError(
                "Год должен быть целым числом и не больше текущего года."
            )

        # Валидация status
        if self.status not in (s.value for s in Status):
            raise ValueError(
                "Статус книги должен быть одним из: "
                f"{', '.join(s.value for s in Status)}"
            )

    def __str__(self):
        return (
            f"id: {self.id}\n"
            f"title: {self.title}\n"
            f"author: {self.author}\n"
            f"year: {self.year}\n"
            f"status: {self.status}"
        )

    def __eq__(self, other):
        """Метод сравнения объектов по полям title, author, year."""
        if not isinstance(other, Book):
            return NotImplemented
        return (
            self.title.lower() == other.title.lower()
            and self.author.lower() == other.author.lower()
            and self.year == other.year
        )

    def to_dict(self) -> dict[str, str | int]:
        """Преобразование объекта в словарь."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, str | int]) -> "Book":
        """Классовый метод для создания объекта из словаря."""
        return cls(
            id=data.get("id", 0),
            title=str(data.get("title", "")),
            author=str(data.get("author", "")),
            year=data.get("year", date.today().year),
            status=data.get("status", Status.AVAILABLE.value),
        )

    @staticmethod
    def validate_non_empty_string(field_name: str, value: str) -> str:
        """Валидатор проверяет, что атрибут является непустой строкой."""
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError(
                f"Поле {field_name} должно быть непустой строкой."
            )
        return value.strip()
