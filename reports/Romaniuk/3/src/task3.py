import os
from abc import ABC, abstractmethod


class EncryptionStrategy(ABC):
    @abstractmethod
    def encrypt(self, text: str) -> str:
        pass

    @abstractmethod
    def decrypt(self, text: str) -> str:
        pass


# стратегия 1: вырезаем гласные
class RemoveVowelsStrategy(EncryptionStrategy):
    def encrypt(self, text: str) -> str:
        vowels = "aeiouyаеёиоуыэюяAEIOUYАЕЁИОУЫЭЮЯ"
        result = "".join(ch for ch in text if ch not in vowels)
        return result

    def decrypt(self, text: str) -> str:
        return text + " [расшифровка невозможна - гласные удалены безвозвратно]"


# стратегия 2: сдвиг букв (Цезарь)
class CaesarShiftStrategy(EncryptionStrategy):
    def __init__(self, shift: int = 4):
        self.shift = shift

    def encrypt(self, text: str) -> str:
        result = []
        for ch in text:
            if "а" <= ch <= "я":
                base = ord("а")
                new_pos = (ord(ch) - base + self.shift) % 32
                result.append(chr(base + new_pos))
            elif "А" <= ch <= "Я":
                base = ord("А")
                new_pos = (ord(ch) - base + self.shift) % 32
                result.append(chr(base + new_pos))
            elif "a" <= ch <= "z":
                base = ord("a")
                new_pos = (ord(ch) - base + self.shift) % 26
                result.append(chr(base + new_pos))
            elif "A" <= ch <= "Z":
                base = ord("A")
                new_pos = (ord(ch) - base + self.shift) % 26
                result.append(chr(base + new_pos))
            else:
                result.append(ch)
        return "".join(result)

    def decrypt(self, text: str) -> str:
        reverse_strategy = CaesarShiftStrategy(-self.shift)
        return reverse_strategy.encrypt(text)


# стратегия 3: XOR с ключом
class XorStrategy(EncryptionStrategy):
    def __init__(self, key: str = "secret"):
        self.key = key

    def encrypt(self, text: str) -> str:
        result = []
        key_len = len(self.key)
        for i, ch in enumerate(text):
            key_char = self.key[i % key_len]
            xor_result = ord(ch) ^ ord(key_char)
            result.append(chr(xor_result))
        return "".join(result)

    def decrypt(self, text: str) -> str:
        return self.encrypt(text)


class FileEncryptor:
    def __init__(self, strategy: EncryptionStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: EncryptionStrategy):
        self.strategy = strategy

    def encrypt_file(self, input_path: str, output_path: str = None):
        if output_path is None:
            name, ext = os.path.splitext(input_path)
            output_path = f"{name}_encrypted{ext}"

        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()

        encrypted = self.strategy.encrypt(text)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(encrypted)

        print(f"Файл зашифрован: {output_path}")
        return output_path

    def decrypt_file(self, input_path: str, output_path: str = None):
        if output_path is None:
            name, ext = os.path.splitext(input_path)
            output_path = f"{name}_decrypted{ext}"

        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()

        decrypted = self.strategy.decrypt(text)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(decrypted)

        print(f"Файл расшифрован: {output_path}")
        return output_path


def interactive_mode():
    """Интерактивный режим - пользователь выбирает алгоритм и файл."""
    print("=" * 60)
    print("ПРОЕКТ «ШИФРОВАНИЕ» — ПАТТЕРН СТРАТЕГИЯ")
    print("=" * 60)

    print("\nВыберите алгоритм шифрования:")
    print("1. Удаление гласных")
    print("2. Сдвиг Цезаря")
    print("3. XOR")

    choice = input("\nВаш выбор (1-3): ")

    if choice == "1":
        strategy = RemoveVowelsStrategy()
        print("Выбрано: удаление гласных")
    elif choice == "2":
        shift = int(input("Введите сдвиг (например, 4): "))
        strategy = CaesarShiftStrategy(shift)
        print(f"Выбрано: сдвиг Цезаря на {shift}")
    elif choice == "3":
        key = input("Введите ключ (например, secret): ")
        strategy = XorStrategy(key)
        print(f"Выбрано: XOR с ключом '{key}'")
    else:
        print("Неверный выбор!")
        return

    encryptor = FileEncryptor(strategy)

    file_path = input("\nВведите путь к файлу для шифрования: ")
    if os.path.exists(file_path):
        encryptor.encrypt_file(file_path)
    else:
        print(f"Файл {file_path} не найден!")


def main():
    interactive_mode()


if __name__ == "__main__":
    main()
