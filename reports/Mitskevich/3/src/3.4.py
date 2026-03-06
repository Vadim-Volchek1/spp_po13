from abc import ABC, abstractmethod
import random
from typing import List


# ПАТТЕРН ИТЕРАТОР
class ComponentIterator(ABC):
    """Абстрактный класс итератора"""

    @abstractmethod
    def has_next(self) -> bool:
        pass

    @abstractmethod
    def next(self):
        pass


class RandomIterator(ComponentIterator):
    """Конкретный итератор для обхода компонентов в случайном порядке"""

    def __init__(self, components: List):
        self._components = components.copy()  # Создаем копию списка
        self._index = 0
        self._shuffle_components()  # Перемешиваем компоненты при создании итератора

    def _shuffle_components(self):
        """Перемешивает компоненты в случайном порядке"""
        random.shuffle(self._components)
        print("    [Итератор: компоненты перемешаны для случайного вывода]")

    def has_next(self) -> bool:
        """Проверяет, есть ли еще элементы для обхода"""
        return self._index < len(self._components)

    def next(self):
        """Возвращает следующий элемент и переходит к следующему"""
        if self.has_next():
            component = self._components[self._index]
            self._index += 1
            return component
        raise StopIteration("Компоненты закончились")


class IterableComponent(ABC):
    """Интерфейс для компонентов, которые можно обойти итератором"""

    @abstractmethod
    def create_iterator(self) -> ComponentIterator:
        pass


class FileSystemComponent(ABC):
    """Абстрактный базовый класс для всех компонентов файловой системы"""

    def __init__(self, nameF, dateF):
        self._name = nameF
        self._date = dateF

    @abstractmethod
    def getSize(self):
        pass

    @abstractmethod
    def display(self, indent=""):
        pass

    def getName(self):
        return self._name

    def getDate(self):
        return self._date

    def add(self, component):
        raise NotImplementedError("Сюда добавлять текст низя :( )")

    def remove(self, component):
        raise NotImplementedError("Удалить низя :( )")

    def getChild(self, index):
        raise NotImplementedError("Упс, что-то пошло не так *_* ")


class Directory(FileSystemComponent, IterableComponent):

    def __init__(self, nameF, dateF):
        super().__init__(nameF, dateF)
        self._children = []

    def add(self, component):
        """Добавление компонента в директорию"""
        if component not in self._children:
            self._children.append(component)
            print(f"{component.getName()} добавлен в папочку {self._name}")
        else:
            print(f"{component.getName()} уже есть в папочке {self._name}")

    def remove(self, component):
        """Удаление компонента из директории"""
        if component in self._children:
            self._children.remove(component)
            print(f"{component.getName()} удален из папочки {self._name}, дасвиданя ;)")

    def getChild(self, index):
        """Получение дочернего компонента по индексу"""
        if 0 <= index < len(self._children):
            return self._children[index]
        return None

    def getChildren(self):
        """Получение всех дочерних компонентов"""
        return self._children.copy()

    def getSize(self):
        """Рекурсивный подсчет размера папки"""
        total_size = 0
        for child in self._children:
            total_size += child.getSize()
        return total_size

    def findByName(self, nameF):
        """Поиск компонента по имени в текущей папке"""
        for child in self._children:
            if child.getName() == nameF:
                return child
        return None

    def display(self, indent=""):
        """Вывод содержимого папки в обычном порядке"""
        print(
            f"{indent} {self._name}/ (размер: {self.getSize()} байт, создан: {self._date})"
        )
        for child in self._children:
            child.display(indent + "  ")

    # Методы для паттерна Итератор
    def create_iterator(self) -> ComponentIterator:
        """Создает итератор для обхода дочерних компонентов"""
        return RandomIterator(self._children)

    def display_random(self, indent=""):
        """Вывод содержимого папки в СЛУЧАЙНОМ порядке с использованием итератора"""
        print(
            f"{indent} {self._name}/ (размер: {self.getSize()} байт, создан: {self._date})"
        )

        # Создаем итератор для случайного обхода
        iterator = self.create_iterator()

        # Используем итератор для обхода компонентов в случайном порядке
        while iterator.has_next():
            child = iterator.next()
            # Для папок рекурсивно вызываем display_random, для файлов - обычный display
            if isinstance(child, Directory):
                child.display_random(indent + "  ")
            else:
                child.display(indent + "  ")


class File(FileSystemComponent):

    def __init__(self, nameF, extensionF, dateF):
        super().__init__(f"{nameF}.{extensionF}", dateF)
        self._name_without_ext = nameF
        self._extension = extensionF
        self._size = 0
        self._content = ""

    def getSize(self):
        return self._size

    def getExtension(self):
        return self._extension

    def addContent(self):
        """Добавление содержимого в файл"""
        if self._extension.lower() == "txt":
            contOfFile = input("Введите содержимое текстового файла: ")
            self._content = contOfFile
            self._size = len(contOfFile.encode("utf-8"))  # Размер в байтах
            print(
                f"Содержимое добавлено в файл {self._name}. Размер: {self._size} байт"
            )
        else:
            print(
                f"Это не текстовый файл (расширение .{self._extension}), вводить низя :("
            )

    def readContent(self):
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
        """Отображение информации о файле с основными атрибутами"""
        print(
            f"{indent} {self._name} (размер: {self._size} байт, создан: {self._date}, расширение: .{self._extension})"
        )


class FileSystem:

    def __init__(self):
        root_date = input(
            "Введите дату создания корневой директории (например, 2024-01-15): "
        )
        self._root = Directory("root", root_date)
        self._current_directory = self._root
        self._current_path = ["root"]

    def getCurrentPath(self):
        return "/" + "/".join(self._current_path)

    def changeDirectory(self, dirname):
        if dirname == "..":
            if len(self._current_path) > 1:
                self._current_path.pop()
                self._current_directory = self._root
                for dir_name in self._current_path[1:]:
                    next_dir = self._current_directory.findByName(dir_name)
                    if next_dir and isinstance(next_dir, Directory):
                        self._current_directory = next_dir
                    else:
                        break
                print(f"Перешли в директорию {self.getCurrentPath()}")
            else:
                print("Уже в корневой директории")
        else:
            target = self._current_directory.findByName(dirname)
            if target and isinstance(target, Directory):
                self._current_directory = target
                self._current_path.append(dirname)
                print(f"Перешли в папочку {self.getCurrentPath()}")
            else:
                print(f"Папка '{dirname}' не найдена, плак плак ((( )")

    def createFile(self, nameF, extensionF):
        filenameF = f"{nameF}.{extensionF}"
        existing = self._current_directory.findByName(filenameF)
        if existing:
            print(f"Файл '{filename}' уже существует")
            return None

        file_date = input(f"Введите дату создания файла {filename}: ")
        new_file = File(name, extensionF, file_date)
        self._current_directory.add(new_file)
        return new_file

    def createDirectory(self, nameF):
        existing = self._current_directory.findByName(nameF)
        if existing:
            print(f"Папка '{nameF}' уже существует")
            return None

        dir_date = input(f"Введите дату создания папки {nameF}: ")
        new_dir = Directory(nameF, dir_date)
        self._current_directory.add(new_dir)
        return new_dir

    def listContents(self):
        """Вывод содержимого текущей папки в обычном порядке"""
        print(f"\nСодержимое {self.getCurrentPath()} (в обычном порядке):")
        if not self._current_directory.getChildren():
            print("  (пусто, выросла капуста, хы)")
        else:
            self._current_directory.display()

    def listContentsRandom(self):
        """Вывод содержимого текущей папки в СЛУЧАЙНОМ порядке с использованием итератора"""
        print(f"\n Содержимое {self.getCurrentPath()} (В СЛУЧАЙНОМ ПОРЯДКЕ):")
        if not self._current_directory.getChildren():
            print("  (пусто, выросла капуста, хы)")
        else:
            self._current_directory.display_random()

    def findFile(self, filenameF):
        return self._current_directory.findByName(filenameF)

    def deleteItem(self, nameF):
        item = self._current_directory.findByName(nameF)
        if item:
            self._current_directory.remove(item)
        else:
            print(f"'{nameF}' не найден в текущей папке, какой ужассс")

    def getCurrentDirectory(self):
        return self._current_directory

    def display_root_tree(self, random_order=False):
        """Показать дерево от корня"""
        print(
            "\nПолное дерево файловой системы",
            "(СЛУЧАЙНЫЙ ПОРЯДОК):" if random_order else "(обычный порядок):",
        )

        if random_order:
            self._root.display_random()
        else:
            self._root.display()


def Menu():
    print("*" * 60)
    print("КОМАНДЫ:")
    print("  ls              - показать содержимое (в обычном порядке)")
    print("  ls-random       - показать содержимое В СЛУЧАЙНОМ ПОРЯДКЕ (с итератором)")
    print("  cd <директория> - перейти в директорию")
    print("  cd ..           - перейти в родительскую директорию")
    print("  mkdir <имя>     - создать директорию")
    print("  touch <имя>.<расш> - создать файл")
    print("  write <файл>    - добавить содержимое в txt файл")
    print("  read <файл>     - прочитать содержимое txt файла")
    print("  rm <имя>        - удалить файл/директорию")
    print("  pwd             - показать текущий путь")
    print("  tree            - показать всё дерево от корня (обычный порядок)")
    print("  tree-random     - показать всё дерево В СЛУЧАЙНОМ ПОРЯДКЕ")
    print("  help            - показать команды")
    print("  exit            - выход")
    print("*" * 60)


# Интерактивный интерфейс
print("*" * 60)
print("ФАЙЛОВАЯ СИСТЕМА 2.0 с ПАТТЕРНОМ ИТЕРАТОР ")
print("*" * 60)
Menu()

fs = FileSystem()

while True:
    command = input(f"\n{fs.getCurrentPath()}> ").strip().split()

    if not command:
        continue

    cmd = command[0].lower()

    if cmd == "help":
        Menu()

    elif cmd == "ls":
        fs.listContents()

    elif cmd == "ls-random":
        fs.listContentsRandom()

    elif cmd == "pwd":
        print(fs.getCurrentPath())

    elif cmd == "tree":
        print("\nПолное дерево файловой системы (обычный порядок):")
        fs.display_root_tree(random_order=False)

    elif cmd == "tree-random":
        print("\nПолное дерево файловой системы (СЛУЧАЙНЫЙ ПОРЯДОК):")
        fs.display_root_tree(random_order=True)

    elif cmd == "cd":
        if len(command) < 2:
            print("Укажите папочку")
        else:
            fs.changeDirectory(command[1])

    elif cmd == "mkdir":
        if len(command) < 2:
            print("Укажите имя папочки")
        else:
            fs.createDirectory(command[1])

    elif cmd == "touch":
        if len(command) < 2:
            print("Укажите имя файла с расширением")
        else:
            filename = command[1]
            if "." in filename:
                name, ext = filename.rsplit(".", 1)
                fs.createFile(name, ext)
            else:
                print("Файл должен иметь расширение")

    elif cmd == "write":
        if len(command) < 2:
            print("Укажите имя файла")
        else:
            file_item = fs.findFile(command[1])
            if file_item and isinstance(file_item, File):
                file_item.addContent()
            else:
                print(f"Файл '{command[1]}' не найден")

    elif cmd == "read":
        if len(command) < 2:
            print("Укажите имя файла")
        else:
            file_item = fs.findFile(command[1])
            if file_item and isinstance(file_item, File):
                file_item.readContent()
            else:
                print(f"Файл '{command[1]}' не найден")

    elif cmd == "rm":
        if len(command) < 2:
            print("Укажите имя файла или директории")
        else:
            fs.deleteItem(command[1])

    elif cmd == "exit":
        print("До свиданя!")
        break

    else:
        print(f"Неизвестная команда: {cmd}")
