from abc import ABC, abstractmethod
import os
from typing import Optional

class EncryptionStrategy(ABC):
    """Абстрактный класс стратегии шифрования"""

    @abstractmethod
    def encrypt(self, text: str) -> str:
        """Зашифровать текст"""
        pass

    @abstractmethod
    def decrypt(self, text: str) -> str:
        """Расшифровать текст"""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Название алгоритма"""
        pass


# ============= Конкретные стратегии =============
class VowelRemovalStrategy(EncryptionStrategy):
    """Стратегия: удаление всех гласных букв"""

    def __init__(self):
        self._vowels = set('aeiouyаеёиоуыэюяAEIOUYАЕЁИОУЫЭЮЯ')

    def encrypt(self, text: str) -> str:
        return ''.join(char for char in text if char not in self._vowels)

    def decrypt(self, text: str) -> str:
        return f"[Невозможно восстановить гласные] {text}"

    @property
    def name(self) -> str:
        return "Удаление гласных"


class CaesarShiftStrategy(EncryptionStrategy):
    """Стратегия: сдвиг букв на фиксированное число"""

    def __init__(self, shift: int = 20):
        self.shift = shift

        self.ru_lower = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        self.ru_upper = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

        self.en_lower = 'abcdefghijklmnopqrstuvwxyz'
        self.en_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def _shift_char(self, char: str, alphabet: str, shift: int) -> str:
        """Сдвигает символ в пределах алфавита"""
        if char in alphabet:
            idx = alphabet.index(char)
            new_idx = (idx + shift) % len(alphabet)
            return alphabet[new_idx]
        return char

    def encrypt(self, text: str) -> str:
        """Сдвигает буквы вперед на shift позиций"""
        result = []
        for char in text:
            if char in self.ru_lower:
                result.append(self._shift_char(char, self.ru_lower, self.shift))
            elif char in self.ru_upper:
                result.append(self._shift_char(char, self.ru_upper, self.shift))
            elif char in self.en_lower:
                result.append(self._shift_char(char, self.en_lower, self.shift))
            elif char in self.en_upper:
                result.append(self._shift_char(char, self.en_upper, self.shift))
            else:
                result.append(char)
        return ''.join(result)

    def decrypt(self, text: str) -> str:
        """Сдвигает буквы назад на shift позиций"""
        result = []
        for char in text:
            if char in self.ru_lower:
                result.append(self._shift_char(char, self.ru_lower, -self.shift))
            elif char in self.ru_upper:
                result.append(self._shift_char(char, self.ru_upper, -self.shift))
            elif char in self.en_lower:
                result.append(self._shift_char(char, self.en_lower, -self.shift))
            elif char in self.en_upper:
                result.append(self._shift_char(char, self.en_upper, -self.shift))
            else:
                result.append(char)
        return ''.join(result)

    @property
    def name(self) -> str:
        return f"Сдвиг на {self.shift}"


class XorStrategy(EncryptionStrategy):
    """Стратегия: XOR с заданным ключом"""

    def __init__(self, key: str = "чебурашка"):
        self.key = key
        # Преобразуем ключ в байт
        self.key_bytes = key.encode('utf-8')

    def _xor_operation(self, data: bytes) -> bytes:
        key_len = len(self.key_bytes)
        result = bytearray()

        for i, byte in enumerate(data):
            result.append(byte ^ self.key_bytes[i % key_len])

        return bytes(result)

    def encrypt(self, text: str) -> str:
        """
        Шифрует текст с помощью XOR
        Возвращает строку в шестнадцатеричном представлении
        """
        text_bytes = text.encode('utf-8')
        encrypted_bytes = self._xor_operation(text_bytes)
        return encrypted_bytes.hex()

    def decrypt(self, text: str) -> str:
        """
        Расшифровывает текст из шестнадцатеричного представления
        """
        try:
            encrypted_bytes = bytes.fromhex(text)
            decrypted_bytes = self._xor_operation(encrypted_bytes)
            return decrypted_bytes.decode('utf-8')
        except (ValueError, UnicodeDecodeError) as e:
            return f"[Ошибка расшифровки: {e}]"

    @property
    def name(self) -> str:
        return f"XOR (ключ: {self.key})"


# ============= Контекст (класс-шифровщик) =============
class FileEncryptor:
    """Шифровщик текстовых файлов"""

    def __init__(self, strategy: Optional[EncryptionStrategy] = None):
        """
        :param strategy: стратегия шифрования
        """
        self._strategy = strategy

    def set_strategy(self, strategy: EncryptionStrategy) -> None:
        """Сменить стратегию шифрования"""
        self._strategy = strategy

    def encrypt_file(self, input_path: str, output_path: str) -> bool:
        """
        Зашифровать файл

        :param input_path: путь к исходному файлу
        :param output_path: путь к зашифрованному файлу
        :return: True в случае успеха, False при ошибке
        """
        if not self._strategy:
            raise ValueError("Стратегия шифрования не установлена")

        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()

            encrypted_content = self._strategy.encrypt(content)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(encrypted_content)

            return True

        except FileNotFoundError:
            print(f"Ошибка: файл {input_path} не найден")
            return False
        except Exception as e:
            print(f"Ошибка при шифровании: {e}")
            return False

    def decrypt_file(self, input_path: str, output_path: str) -> bool:
        """
        Расшифровать файл

        :param input_path: путь к зашифрованному файлу
        :param output_path: путь к расшифрованному файлу
        :return: True в случае успеха, False при ошибке
        """
        if not self._strategy:
            raise ValueError("Стратегия шифрования не установлена")

        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()

            decrypted_content = self._strategy.decrypt(content)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(decrypted_content)

            return True

        except FileNotFoundError:
            print(f"Ошибка: файл {input_path} не найден")
            return False
        except Exception as e:
            print(f"Ошибка при расшифровке: {e}")
            return False

    def get_current_strategy_name(self) -> str:
        """Получить название текущей стратегии"""
        return self._strategy.name if self._strategy else "Не установлена"

def main():
    """Демонстрация работы шифровщика"""

    # Создаем тестовый файл
    test_file = "test_input.txt"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("Привет, мир! Hello, world!\n")
        f.write("Это тестовый файл для шифрования.\n")
        f.write("XOR encryption test with key: чебурашка")

    encryptor = FileEncryptor()

    # ===== Тест 1: Удаление гласных =====
    print("=" * 50)
    print("Тест 1: Удаление гласных")
    encryptor.set_strategy(VowelRemovalStrategy())
    print(f"Стратегия: {encryptor.get_current_strategy_name()}")

    encryptor.encrypt_file("test_input.txt", "test_vowel_removed.txt")
    encryptor.decrypt_file("test_vowel_removed.txt", "test_vowel_decoded.txt")

    with open("test_vowel_removed.txt", 'r', encoding='utf-8') as f:
        print("Зашифровано:")
        print(f.read())

    # ===== Тест 2: Сдвиг на M =====
    print("\n" + "=" * 50)
    print("Тест 2: Сдвиг на 3")
    encryptor.set_strategy(CaesarShiftStrategy(shift=3))
    print(f"Стратегия: {encryptor.get_current_strategy_name()}")

    encryptor.encrypt_file("test_input.txt", "test_caesar.txt")
    encryptor.decrypt_file("test_caesar.txt", "test_caesar_decoded.txt")

    print("Расшифрованный файл:")
    with open("test_caesar_decoded.txt", 'r', encoding='utf-8') as f:
        print(f.read())

    # ===== Тест 3: XOR с ключом =====
    print("\n" + "=" * 50)
    print("Тест 3: XOR с ключом 'чебурашка'")
    encryptor.set_strategy(XorStrategy(key="чебурашка"))
    print(f"Стратегия: {encryptor.get_current_strategy_name()}")

    encryptor.encrypt_file("test_input.txt", "test_xor.txt")

    with open("test_xor.txt", 'r', encoding='utf-8') as f:
        print("Зашифровано (hex):")
        print(f.read()[:100] + "...")

    encryptor.decrypt_file("test_xor.txt", "test_xor_decoded.txt")

    print("\nРасшифрованный файл:")
    with open("test_xor_decoded.txt", 'r', encoding='utf-8') as f:
        print(f.read())

    # ===== Тест 4: Смена стратегии на лету =====
    print("\n" + "=" * 50)
    print("Тест 4: Смена стратегии на лету")
    encryptor.set_strategy(CaesarShiftStrategy(shift=10))
    print(f"Новая стратегия: {encryptor.get_current_strategy_name()}")
    encryptor.encrypt_file("test_input.txt", "test_caesar_10.txt")
    print("Файл зашифрован со сдвигом 10")

    encryptor.decrypt_file("test_caesar_10.txt", "test_caesar_10_decoded.txt")

    print("Расшифрованный файл:")
    with open("test_caesar_10_decoded.txt", 'r', encoding='utf-8') as f:
        print(f.read())

if __name__ == "__main__":
    main()
