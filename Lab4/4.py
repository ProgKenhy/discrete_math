# -*- coding: utf-8 -*-
from collections import Counter

def analyze_text(text_file, allowed_chars):
    """
    Анализирует текстовый файл, проводя статистику частоты символов и пар символов.

    Args:
        text_file (str): Путь к текстовому файлу.
        allowed_chars (str): Строка, содержащая разрешенные символы.
    """

    try:
        # Чтение текста из файла
        with open(text_file, 'r', encoding='utf-8') as f:
            text = f.read().lower()  # Читаем, переводим в нижний регистр

        # Очистка текста: оставляем только разрешенные символы
        cleaned_text = ''.join(c for c in text if c in allowed_chars)

        # Проверяем длину текста (примерно 16000 символов)
        text_length = len(cleaned_text)
        print(f"Длина текста после очистки: {text_length} символов")

        # Проверка длины текста
        if text_length < 15000 or text_length > 17000:
            print("Внимание: Длина текста выходит за рекомендуемые рамки (15000-17000 символов).")

        # Статистика частоты отдельных символов
        char_counts = Counter(cleaned_text)
        print("\nСтатистика частоты отдельных символов:")
        for char, count in char_counts.most_common():
            print(f"{char}: {count}")

        # Статистика частоты пар символов (диграфов)
        digraph_counts = Counter(cleaned_text[i: i + 2] for i in range(len(cleaned_text) - 1))
        print("\nСтатистика частоты пар символов (диграфов):")
        for digraph, count in digraph_counts.most_common(20):  # Выводим топ-20 диграфов
            print(f"{digraph}: {count}")

    except FileNotFoundError:
        print(f"Ошибка: Файл '{text_file}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# --- Пример использования ---

# 1. Путь к текстовому файлу.
file_path = "text_file.txt"  # Замените на реальный путь к файлу!

# 2. Определение разрешенных символов. Включаем буквы, пробел, знаки препинания, цифры.
allowed_characters = "abcdefghijklmnopqrstuvwxyz .,!?"  # Расширенный набор

# 3. Запуск анализа.
analyze_text(file_path, allowed_characters)
