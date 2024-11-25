import json
from typing import List, Dict, Union, Optional


DATA_FILE = "data.json"


class Book:
    """ Класс, представляющий книгу в библиотеке """
    def __init__(self, book_id: int, title: str, author: str, year: int, status: str = "в наличии"):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> Dict[str, Union[int, str]]:
        """
        Преобразует объект книги в словарь.

        Returns:
            dict: Словарь с данными о книге.
        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data: Dict[str, Union[int, str]]) -> 'Book':
        """
        Создает объект книги из словаря.

        Args:
            data (dict): Словарь с данными о книге.

        Returns:
            Book: Новый экземпляр книги.
        """
        return Book(
            book_id=data["id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            status=data["status"],
        )

    @staticmethod
    def validate_dict(data: Dict[str, Union[int, str]]) -> bool:
        """
        Проверяет, соответствует ли словарь ожидаемому формату книги.

        Args:
            data (dict): Словарь с данными книги.

        Returns:
            bool: True, если данные валидны, иначе False.
        """
        required_fields = {"id": int, "title": str, "author": str, "year": int, "status": str}
        valid_statuses = {"в наличии", "выдана"}

        for field, field_type in required_fields.items():
            if field not in data or not isinstance(data[field], field_type):
                return False

        if data["status"] not in valid_statuses:
            return False

        return True


class Library:
    """
    Класс, представляющий библиотеку книг.

    Атрибуты:
        data_file (str): Имя файла для хранения данных.
        Books (List[Book]): Список книг в библиотеке.
    """
    def __init__(self, data_file: str = DATA_FILE):
        self.data_file = data_file
        self.books = self.load_books()

    def load_books(self) -> List[Book]:
        """
        Загружает данные книг из файла и валидирует их.

        Returns:
            List[Book]: Список объектов книг.
        """
        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                data = json.load(file)
            books = []
            for raw_book in data:
                if Book.validate_dict(raw_book):
                    books.append(Book.from_dict(raw_book))
                else:
                    print(f"Ошибка: некорректные данные книги {raw_book}. Пропущено.")
            return books
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("Ошибка чтения данных. Создается новая библиотека.")
            return []

    def _save_books(self):
        """ Сохраняет данные книг в файл. """
        with open(self.data_file, "w", encoding="utf-8") as file:
            json.dump(
                [book.to_dict() for book in self.books],
                file,
                ensure_ascii=False,
                indent=4
            )

    def add_book(self, title: str, author: str, year: int) -> Book:
        """
        Добавляет новую книгу в библиотеку.

        Args:
            title (str): Название книги.
            author (str): Автор книги.
            year (int): Год издания.
        Returns:
            Book: книга
        """
        book_id = (max([book.id for book in self.books], default=0) + 1)
        new_book = Book(book_id, title, author, year)
        self.books.append(new_book)
        self._save_books()
        print(f"Книга '{title}' добавлена с ID {book_id}.")
        return new_book

    def delete_book(self, book_id: int):
        """
        Удаляет книгу по её ID.

        Args:
            book_id (int): ID книги.
        """
        book = self.find_book_by_id(book_id)
        if book:
            self.books.remove(book)
            self._save_books()
            print(f"Книга с ID {book_id} удалена.")
        else:
            print(f"Книга с ID {book_id} не найдена.")

    def find_book_by_id(self, book_id: int) -> Optional[Book]:
        """
        Ищет книгу по ID.

        Args:
            book_id (int): ID книги.

        Returns:
            Optional[Book]: Найденная книга или None, если книга не найдена.
        """
        return next((book for book in self.books if book.id == book_id), None)

    def search_books(self, keyword: str):
        """
        Ищет книги по ключевому слову.

        Args:
            keyword (str): Ключевое слово для поиска (название, автор, год).
        """
        results = [book for book in self.books if keyword.lower() in book.title.lower() or
                   keyword.lower() in book.author.lower() or
                   str(book.year) == keyword]
        if results:
            self.display_books(results)
        else:
            print("Книги по вашему запросу не найдены.")


    def find_books(self, books: Optional[List[Book]] = None) -> Optional[List[Book]]:
        """
        Возвращает список книг.

        Args:
           books (Optional[List[Book]]): Список книг для поиска. Если None, возвращаются все книги.
        """
        books = books or self.books
        if not books:
            return None
        return books


    def display_books(self, books: Optional[List[Book]] = None):
        """
        Отображает список книг.

        Args:
            books (Optional[List[Book]]): Список книг для отображения. Если None, отображаются все книги.
        """
        books = books or self.books
        if not books:
            print("Библиотека пуста.")
            return
        for book in books:
            print(f"ID: {book.id} | Название: {book.title} | Автор: {book.author} | Год: {book.year} | Статус: {book.status}")

    def update_status(self, book_id: int, new_status: str):
        """
        Обновляет статус книги.

        Args:
            book_id (int): ID книги.
            new_status (str): Новый статус ('в наличии' или 'выдана').
        """
        book = self.find_book_by_id(book_id)
        if book:
            if new_status in ["в наличии", "выдана"]:
                book.status = new_status
                self._save_books()
                print(f"Статус книги с ID {book_id} изменен на '{new_status}'.")
            else:
                print("Некорректный статус. Допустимые статусы: 'в наличии', 'выдана'.")
        else:
            print(f"Книга с ID {book_id} не найдена.")


def main():
    library = Library()

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Поиск книги")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = int(input("Введите год издания: "))
            library.add_book(title, author, year)
        elif choice == "2":
            book_id = int(input("Введите ID книги для удаления: "))
            library.delete_book(book_id)
        elif choice == "3":
            keyword = input("Введите ключевое слово для поиска (название, автор или год): ")
            library.search_books(keyword)
        elif choice == "4":
            library.display_books()
        elif choice == "5":
            if not library.find_books():
                print("Библиотека пуста.")
                continue
            try:
                book_id = int(input("Введите ID книги: "))
                if library.find_book_by_id(book_id) is None:
                    print(f"Книга с ID {book_id} не найдена.")
                    continue
                print("Выберите новый статус:")
                print("1. в наличии")
                print("2. выдана")
                status_choice = int(input("Введите номер: "))

                if status_choice == 1:
                    new_status = "в наличии"
                elif status_choice == 2:
                    new_status = "выдана"
                else:
                    print("Ошибка: некорректный выбор статуса.")
                    continue

                library.update_status(book_id, new_status)
                print("Статус книги успешно обновлён.")
            except ValueError:
                print("Ошибка: некорректный ввод. Убедитесь, что вводите числа.")
        elif choice == "6":
            print("Выход из программы.")
            break
        else:
            print("Некорректный ввод. Попробуйте снова.")


if __name__ == "__main__":
    main()
