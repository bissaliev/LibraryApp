from json import JSONDecodeError
from typing import Callable

from books import Book, Status
from filemanagers import JsonFileManager
from libraries import LibraryManager

menu_items: dict[str, str] = {
    "1": "Показать все книги",
    "2": "Получить книгу по ID",
    "3": "Добавить книгу",
    "4": "Удалить книгу",
    "5": "Изменить статус книги",
    "6": "Найти книгу",
    "7": "Выход",
}


def display_menu() -> None:
    """Отображение меню."""
    print("\n" + "-" * 30)
    for key, value in menu_items.items():
        print(f"{key}. {value}")
    print("-" * 30)


def get_int_input(prompt: str) -> int:
    """Получение числового значения от пользователя с обработкой ошибок."""
    try:
        return int(input(prompt).strip())
    except ValueError as error:
        raise ValueError("Ввод должен быть числом.") from error


def get_input(prompt: str) -> str:
    """Получение ввода пользователя."""
    return input(prompt).strip()


def display_books(library: LibraryManager) -> None:
    """Отображение всех книг."""
    books: list[Book] = library.get_books()
    if not books:
        print("\nВ библиотеке пока нет книг.\n")
    else:
        print("\n\n".join(str(book) for book in books))


def display_book_by_id(library: LibraryManager) -> None:
    """Отображение книги по ID."""
    try:
        book_id = get_int_input("Введите ID нужной книги: ")
        book: Book = library.get_book(book_id)
        print(f"\nНайдена книга:\n{book}\n")
    except ValueError as error:
        print(f"\nОшибка: {error}\n")


def add_book(library: LibraryManager) -> None:
    """Добавление новой книги в библиотеку."""
    title = get_input("Введите заголовок книги: ")
    author = get_input("Введите автора книги: ")
    try:
        year = get_int_input("Введите год публикации книги: ")
        new_book: Book = library.add_book(title, author, year)
        print(f"\nДобавлена новая книга в библиотеку:\n{new_book}\n")
    except ValueError as error:
        print(f"\nОшибка: {error}\n")


def delete_book(library: LibraryManager) -> None:
    """Удаление книги по ID."""
    try:
        book_id = get_int_input("Введите id книги которую хотите удалить: ")
        remote_book: Book = library.delete_book(book_id)
        print(f"\nКнига удалена:\n{remote_book}\n")
    except ValueError as error:
        print(f"\nОшибка: {error}\n")


def update_status_of_book(library: LibraryManager) -> None:
    """Обновление статуса книги."""
    try:
        book_id = get_int_input("Введите id книги, которую хотите изменить: ")
        print("\n".join(f"{i}. {s.value}" for i, s in enumerate(Status, 1)))
        option = get_int_input("Выберите число нужного варианта: ") - 1
        try:
            new_status = list(Status)[option].value
        except IndexError as error:
            raise ValueError("Выбран неверный вариант.") from error
        updated_book: Book = library.update_book_status(book_id, new_status)
        print(f"\nСтатус книги изменен:\n{updated_book}\n")
    except ValueError as error:
        print(f"\nОшибка: {error}\n")


def search_book(library: LibraryManager) -> None:
    """Поиск книг по названию, автору и году."""
    search_fields = dict(enumerate(library.search_fields, 1))
    print("\n".join(f"{num}. {field}" for num, field in search_fields.items()))
    try:
        option = get_int_input(
            "Введите номер поля по которому нужно найти книгу: "
        )
        field = search_fields.get(option)
        if field:
            prompt = f"Введите значение для поиска в поле {field}: "
            query = (
                get_int_input(prompt) if field == "year" else get_input(prompt)
            )
            books: list[Book] = library.search_book(field, query)
            print(f"\nПо вашему запросу найдено {len(books)} совпадений:\n")
            print("\n\n".join(str(book) for book in books))
        else:
            print("\nОшибка: Неверный выбор.\n")
    except ValueError as error:
        print(f"\nОшибка: {error}\n")


actions: dict[str, Callable[[LibraryManager], None]] = {
    "1": display_books,
    "2": display_book_by_id,
    "3": add_book,
    "4": delete_book,
    "5": update_status_of_book,
    "6": search_book,
}


def main():
    """Точка входа."""
    try:
        file_manager = JsonFileManager("library.json")
        library = LibraryManager(Book, file_manager)
        while True:
            try:
                display_menu()
                choice = input("Введите число выбора: ")
                if choice == "7":
                    print("\nДо свидания!!!\n")
                    break
                action = actions.get(choice)
                if action:
                    action(library)
                else:
                    print("Вы ввели некорректное значение.")
            except Exception as error:
                print(f"\nОшибка: {error}\n")
    except FileNotFoundError as error:
        print(f"Ошибка: {error}")
    except JSONDecodeError as error:
        print(f"Ошибка: {error}")
    except Exception as error:
        print(f"Произошла неизвестная ошибка: {error}")
    finally:
        print("Программа завершена")


if __name__ == "__main__":
    main()
