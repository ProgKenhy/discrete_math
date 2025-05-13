from collections import Counter
import heapq  # Для алгоритма Хаффмана

class Node:  # Добавлен класс Node
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):  # Для сравнения узлов в очереди с приоритетами
        return self.freq < other.freq

def build_huffman_tree(frequencies):
    """Строит дерево Хаффмана на основе частот."""
    heap = [Node(char, freq) for char, freq in frequencies.items()]
    heapq.heapify(heap)  # Преобразует список в кучу

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        merged = Node(None, left.freq + right.freq)  # char = None для промежуточных узлов
        merged.left = left
        merged.right = right

        heapq.heappush(heap, merged)

    return heap[0]  # Корень дерева

def generate_huffman_codes(tree, code="", codes={}):  # Добавлен codes={} как аргумент по умолчанию
    """Рекурсивно генерирует коды Хаффмана, заполняя словарь."""
    if tree is None:
        return

    if tree.char is not None:  # Достигли листового узла (символа)
        codes[tree.char] = code
        return

    generate_huffman_codes(tree.left, code + "0", codes) # Передаем словарь codes
    generate_huffman_codes(tree.right, code + "1", codes) # Передаем словарь codes
    return codes

def analyze_text(text_file, allowed_chars):
    """
    Анализирует текстовый файл, проводя статистику частоты символов и пар символов,
    строит коды Хаффмана, выводит таблицу кодов и кодирует текст.
    """

    try:
        # Чтение текста из файла
        with open(text_file, 'r', encoding='utf-8') as f:
            text = f.read().lower()

        # Очистка текста
        cleaned_text = ''.join(c for c in text if c in allowed_chars)
        text_length = len(cleaned_text)
        print(f"Длина текста после очистки: {text_length} символов")

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

        # --- Коды Хаффмана (буквы) ---
        print("\n--- Кодирование Хаффмана (отдельные символы) ---")

        # Построение дерева Хаффмана
        huffman_tree = build_huffman_tree(char_counts)

        # Генерация кодов Хаффмана
        huffman_codes = generate_huffman_codes(huffman_tree)

        # Вывод таблицы кодов
        print("\nТаблица кодов Хаффмана:")
        for char, code in sorted(huffman_codes.items()):
            print(f"{char}: {code}")

        # Кодирование текста
        encoded_text = "".join(huffman_codes[char] for char in cleaned_text)
        encoded_length = len(encoded_text)
        print(f"\nЗакодированный текст (первые 50 символов): {encoded_text[:50]}...")
        print(f"Общая длина закодированного текста (Хаффман): {encoded_length} бит")

        # --- Сравнение с равномерным кодированием ---
        num_unique_chars = len(char_counts)
        uniform_code_length = 5  # Используем 5-битное кодирование

        uniform_encoded_length = text_length * uniform_code_length
        print(f"\nДлина закодированного текста (равномерное {uniform_code_length}-битное кодирование): {uniform_encoded_length} бит")

        # --- Сравнение и вывод результатов ---
        compression_ratio = uniform_encoded_length / encoded_length
        print(f"\nКоэффициент сжатия (равномерное/Хаффман): {compression_ratio:.2f}")
        if encoded_length < uniform_encoded_length:
            print("Кодирование Хаффмана эффективнее!")
        else:
            print("Равномерное кодирование эффективнее!")

    except FileNotFoundError:
        print(f"Ошибка: Файл '{text_file}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


# --- Пример использования ---
file_path = "text_file.txt"  # Замените на реальный путь к файлу!
allowed_characters = "abcdefghijklmnopqrstuvwxyz .,!?'-0123456789"
analyze_text(file_path, allowed_characters)
