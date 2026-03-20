from abc import ABC, abstractmethod


class FileSystemComponent(ABC):
    """Абстрактный базовый класс для всех компонентов файловой системы"""

    def __init__(self, name, date):
        self._name = name
        self._date = date

    @abstractmethod
    def get_size(self):
        pass

    @abstractmethod
    def display(self, indent=""):
        pass

    def get_name(self):
        return self._name

    def get_date(self):
        return self._date

    def add(self, component):
        raise NotImplementedError("Сюда добавлять текст низя :( )")

    def remove(self, component):
        raise NotImplementedError("Удалить низя :( )")

    def get_child(self, index):
        raise NotImplementedError("Упс, что-то пошло не так *_* ")


class Directory(FileSystemComponent):
    """Класс папочки"""

    def __init__(self, dir_name, date):
        super().__init__(dir_name, date)
        self._children = []

    def add(self, component):
        """Добавление компонента в директорию"""
        if component not in self._children:
            self._children.append(component)
            print(f"{component.get_name()} добавлен в папочку {self._name}")
        else:
            print(f"{component.get_name()} уже есть в папочке {self._name}")

    def remove(self, component):
        """Удаление компонента из директории"""
        if component in self._children:
            self._children.remove(component)
            print(
                f"{component.get_name()} удален из папочки {self._name}, дасвиданя ;)"
            )

    def get_child(self, index):
        """Получение дочернего компонента по индексу"""
        if 0 <= index < len(self._children):
            return self._children[index]
        return None

    def get_children(self):
        """Получение всех дочерних компонентов"""
        return self._children.copy()

    def get_size(self):
        """Рекурсивный подсчет размера папки"""
        total_size = 0
        for child in self._children:
            total_size += child.get_size()
        return total_size

    def find_by_name(self, name):
        """Поиск компонента по имени в текущей папке"""
        for child in self._children:
            if child.get_name() == name:
                return child
        return None

    def display(self, indent=""):
        """Вывод содержимого папки"""
        print(
            f"{indent}{self._name}/ (размер: {self.get_size()} байт, создан: {self._date})"
        )
        for child in self._children:
            child.display(indent + "  ")


class File(FileSystemComponent):
    """Класс файл"""

    def __init__(self, file_name, extension, date):
        super().__init__(f"{file_name}.{extension}", date)
        self._name_without_ext = file_name
        self._extension = extension
        self._size = 0
        self._content = ""

    def get_size(self):
        return self._size

    def get_extension(self):
        return self._extension

    def add_content(self):
        """Добавление содержимого в файл"""
        if self._extension.lower() == "txt":
            content = input("Введите содержимое текстового файла: ")
            self._content = content
            self._size = len(content.encode("utf-8"))  # Размер в байтах
            print(
                f"Содержимое добавлено в файл {self._name}. Размер: {self._size} байт"
            )
        else:
            print(
                f"Это не текстовый файл (расширение .{self._extension}), вводить низя :("
            )

    def read_content(self):
        """Чтение содержимого файла"""
        if self._extension.lower() == "txt" and self._content:
            print(f"\nСодержимое файла {self._name}:")
            print(self._content)
            print()
        elif self._extension.lower() == "txt":
            print(f"Файл {self._name} пуст")
        else:
            print(f"Файл {self._name} - бинарный, прочитать как текст низя :( )")

    def display(self, indent=""):
        """Отображение информации о файле"""
        print(
            f"{indent} {self._name} (размер: {self._size} байт, создан: {self._date})"
        )


class FileSystem:
    """Класс для управления файловой системой в целом"""

    def __init__(self):
        # При создании корня просим пользователя ввести дату
        root_date = input(
            "Введите дату создания корневой директории (например, 2024-01-15): "
        )
        self._root = Directory("root", root_date)
        self._current_directory = self._root
        self._current_path = ["root"]

    def get_current_path(self):
        """Получение текущего пути"""
        return "/" + "/".join(self._current_path)

    def change_directory(self, dir_name):
        """Смена текущей директории"""
        if dir_name == "..":
            self._go_to_parent_directory()
            return

        self._go_to_child_directory(dir_name)


    def _go_to_parent_directory(self):
        """Переход в родительскую директорию"""
        if len(self._current_path) <= 1:
            print("Уже в корневой директории")
            return

        self._current_path.pop()
        self._current_directory = self._root

        for dir_name_item in self._current_path[1:]:
            next_dir = self._current_directory.find_by_name(dir_name_item)
            if next_dir and isinstance(next_dir, Directory):
                self._current_directory = next_dir

        print(f"Перешли в директорию {self.get_current_path()}")

    def _go_to_child_directory(self, dir_name):
        """Переход в дочернюю директорию"""
        target = self._current_directory.find_by_name(dir_name)

        if target and isinstance(target, Directory):
            self._current_directory = target
            self._current_path.append(dir_name)
            print(f"Перешли в папочку {self.get_current_path()}")
        else:
            print(f"Папка '{dir_name}' не найдена, плак плак ((( )")

    def create_file(self, file_name, extension):
        """Создание файла в текущей папке"""
        # Проверка на существование файла с таким именем
        full_filename = f"{file_name}.{extension}"
        existing = self._current_directory.find_by_name(full_filename)
        if existing:
            print(f"Файл '{full_filename}' уже существует")
            return None

        # Просим пользователя ввести дату создания файла
        file_date = input(f"Введите дату создания файла {full_filename}: ")
        new_file = File(file_name, extension, file_date)
        self._current_directory.add(new_file)
        return new_file

    def create_directory(self, dir_name):
        """Создание папки в папке"""
        existing = self._current_directory.find_by_name(dir_name)
        if existing:
            print(f"Папка '{dir_name}' уже существует")
            return None

        # Просим пользователя ввести дату создания папки
        dir_date = input(f"Введите дату создания папки {dir_name}: ")
        new_dir = Directory(dir_name, dir_date)
        self._current_directory.add(new_dir)
        return new_dir

    def list_contents(self):
        """Вывод содержимого текущей папки"""
        print(f"\nСодержимое {self.get_current_path()}:")
        if not self._current_directory.get_children():
            print("  (пусто, выросла капуста, хы)")
        else:
            self._current_directory.display()

    def find_file(self, file_name):
        """Поиск файла в текущей папке"""
        return self._current_directory.find_by_name(file_name)

    def delete_item(self, item_name):
        """Удаление файла или папки из текущей папки"""
        item = self._current_directory.find_by_name(item_name)
        if item:
            self._current_directory.remove(item)
        else:
            print(f"'{item_name}' не найден в текущей папке, какой ужассс")

    def get_current_directory(self):
        """Получение объекта текущей папки"""
        return self._current_directory

    def display_full_tree(self):
        """Показать полное дерево от корня"""
        print("\nПолное дерево файловой системы:")
        self._root.display()


def show_menu():
    """Отображение меню команд"""
    print("*" * 50)
    print("Команды:")
    print("  ls              - показать содержимое текущей директории")
    print("  cd <директория> - перейти в директорию")
    print("  cd ..           - перейти в родительскую директорию")
    print("  mkdir <имя>     - создать директорию")
    print("  touch <имя>.<расш> - создать файл")
    print("  write <файл>    - добавить содержимое в txt файл")
    print("  read <файл>     - прочитать содержимое txt файла")
    print("  rm <имя>        - удалить файл/директорию")
    print("  pwd             - показать текущий путь")
    print("  tree            - показать всё дерево от корня")
    print("  help            - показать команды")
    print("  exit            - выход")
    print("*" * 50)


def process_command(fs, command_parts):
    """Обработка введенной команды"""
    if not command_parts:
        return True

    cmd = command_parts[0].lower()

    # Словарь соответствия команд и функций
    command_map = {
        "exit": (handle_exit, 0),
        "help": (handle_help, 0),
        "ls": (handle_ls, 1),
        "pwd": (handle_pwd, 1),
        "tree": (handle_tree, 1),
        "cd": (handle_cd, 2),
        "mkdir": (handle_mkdir, 2),
        "touch": (handle_touch, 2),
        "write": (handle_write, 2),
        "read": (handle_read, 2),
        "rm": (handle_rm, 2),
    }

    if cmd not in command_map:
        print(f"Неизвестная команда: {cmd}")
        return True

    func, arg_count = command_map[cmd]

    # Вызываем функцию с нужным количеством аргументов
    if arg_count == 0:
        result = func()
    elif arg_count == 1:
        result = func(fs)
    else:  # arg_count == 2
        result = func(fs, command_parts)

    return result if result is not None else True


def handle_exit():
    """Обработка команды exit"""
    print("До свидания!")
    return False


def handle_help():
    """Обработка команды help"""
    show_menu()
    return True


def handle_ls(fs):
    """Обработка команды ls"""
    fs.list_contents()
    return True


def handle_pwd(fs):
    """Обработка команды pwd"""
    print(fs.get_current_path())
    return True


def handle_tree(fs):
    """Обработка команды tree"""
    fs.display_full_tree()
    return True


def handle_cd(fs, command_parts):
    """Обработка команды cd"""
    if len(command_parts) < 2:
        print("Укажите папочку")
    else:
        fs.change_directory(command_parts[1])
    return True


def handle_mkdir(fs, command_parts):
    """Обработка команды mkdir"""
    if len(command_parts) < 2:
        print("Укажите имя папочки")
    else:
        fs.create_directory(command_parts[1])
    return True


def handle_touch(fs, command_parts):
    """Обработка команды touch"""
    if len(command_parts) < 2:
        print("Укажите имя файла с расширением (например: document.txt)")
        return True

    filename = command_parts[1]
    if "." in filename:
        name, ext = filename.rsplit(".", 1)
        fs.create_file(name, ext)
    else:
        print("Файл должен иметь расширение (например: document.txt)")
    return True


def handle_write(fs, command_parts):
    """Обработка команды write"""
    if len(command_parts) < 2:
        print("Укажите имя файла")
        return True

    file_item = fs.find_file(command_parts[1])
    if file_item and isinstance(file_item, File):
        file_item.add_content()
    else:
        print(f"Файл '{command_parts[1]}' не найден")
    return True


def handle_read(fs, command_parts):
    """Обработка команды read"""
    if len(command_parts) < 2:
        print("Укажите имя файла")
        return True

    file_item = fs.find_file(command_parts[1])
    if file_item and isinstance(file_item, File):
        file_item.read_content()
    else:
        print(f"Файл '{command_parts[1]}' не найден")
    return True


def handle_rm(fs, command_parts):
    """Обработка команды rm"""
    if len(command_parts) < 2:
        print("Укажите имя файла или директории")
    else:
        fs.delete_item(command_parts[1])
    return True


def main():
    """Главная функция программы"""
    print("*" * 50)
    print("ФАЙЛОВАЯ СИСТЕМА v1.0")
    print("*" * 50)
    show_menu()

    # Создаем файловую систему с вводом даты для корня
    fs = FileSystem()

    running = True
    while running:
        command = input(f"\n{fs.get_current_path()}> ").strip().split()
        running = process_command(fs, command)


if __name__ == "__main__":
    main()
