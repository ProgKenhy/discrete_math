# -*- coding: utf-8 -*-
import heapq
import math
from collections import Counter

class Node:
    """Представляет узел дерева Хаффмана."""
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char    # Символ, представляемый узлом (для листовых узлов)
        self.freq = freq    # Частота символа
        self.left = left    # Левый дочерний узел
        self.right = right  # Правый дочерний узел

    def __lt__(self, other):
        """Определяет порядок узлов на основе их частоты (для использования в куче)."""
        return self.freq < other.freq

def calculate_char_counts(text, allowed_characters):
    """
    Подсчитывает частоту каждого разрешенного символа в тексте.
    """
    char_counts = Counter(char for char in text.lower() if char in allowed_characters)
    return char_counts

def calculate_digraph_counts(text):
    """Подсчитывает частоту каждой пары символов (диграфов) в тексте."""
    digraph_counts = Counter(text[i:i+2] for i in range(len(text) - 1))
    return digraph_counts

def build_huffman_tree(char_counts):
    """
    Строит дерево Хаффмана на основе частот символов.
    """
    heap = [Node(char=char, freq=freq) for char, freq in char_counts.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged_node = Node(freq=node1.freq + node2.freq, left=node1, right=node2)
        heapq.heappush(heap, merged_node)

    return heap[0]

def generate_huffman_codes(node, current_code="", huffman_codes=None):
    """
    Рекурсивно генерирует коды Хаффмана для каждого символа на основе дерева Хаффмана.
    """
    if huffman_codes is None:
        huffman_codes = {}

    if node.char is not None:
        huffman_codes[node.char] = current_code
        return huffman_codes

    generate_huffman_codes(node.left, current_code + "0", huffman_codes)
    generate_huffman_codes(node.right, current_code + "1", huffman_codes)
    return huffman_codes

def shannon_entropy(char_counts, text_length):
    """
    Вычисляет энтропию Шеннона для текста на основе частот символов.
    """
    entropy = 0.0
    for char, count in char_counts.items():
        probability = float(count) / text_length
        entropy -= probability * math.log2(probability)
    return entropy

def clean_text(text, allowed_characters):
    """Удаляет из текста все символы, кроме разрешенных."""
    cleaned_text = ''.join(char for char in text.lower() if char in allowed_characters)
    return cleaned_text

def analyze_text(file_path, allowed_characters):
    """
    Анализирует текст из файла, вычисляет коды Хаффмана (для символов и диграфов),
    сравнивает с равномерным кодированием и вычисляет энтропию Шеннона.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            original_size = len(text) * 8  # Размер в битах (1 символ = 1 байт = 8 бит)
            text_length = len(text)

            cleaned_text = clean_text(text, allowed_characters)
            cleaned_size = len(cleaned_text) * 8  # Размер очищенного текста в битах
            print(f"Длина очищенного текста: {len(cleaned_text)} символов")
            print(f"Пример очищенного текста: {cleaned_text[:100]}...")

            char_counts = calculate_char_counts(cleaned_text, allowed_characters)
            print("\nЧастоты символов:")
            for char, count in char_counts.most_common():
                print(f"{char}: {count}")

            # --- Huffman Coding for Characters ---
            print("\n--- Huffman Coding for Characters ---")

            huffman_tree_chars = build_huffman_tree(char_counts)
            huffman_codes_chars = generate_huffman_codes(huffman_tree_chars)

            print("\nТаблица кодов Хаффмана (Characters):")
            for char, code in sorted(huffman_codes_chars.items()):
                print(f"{char}: {code}")

            encoded_text_chars = "".join(huffman_codes_chars[char] for char in cleaned_text)
            encoded_length_chars = len(encoded_text_chars)
            print(f"\nЗакодированный текст (первые 50 символов, Characters): {encoded_text_chars[:50]}...")
            print(f"Общая длина закодированного текста (Хаффман, Characters): {encoded_length_chars} бит")

            # --- Huffman Coding for Digraphs ---
            print("\n--- Коды Хаффмана для диграфов ---")

            digraph_counts = calculate_digraph_counts(cleaned_text)
            print("\nЧастоты диграфов:")
            for digraph, count in digraph_counts.most_common(10):
                print(f"{digraph}: {count}")

            huffman_tree_digraphs = build_huffman_tree(digraph_counts)
            huffman_codes_digraphs = generate_huffman_codes(huffman_tree_digraphs)

            print("\nТаблица кодов Хаффмана (Digraphs):")
            for digraph, code in sorted(huffman_codes_digraphs.items()):
                print(f"{digraph}: {code}")

            encoded_text_digraphs = ""
            i = 0
            while i < len(cleaned_text) - 1:
                digraph = cleaned_text[i:i+2]
                if digraph in huffman_codes_digraphs:
                    encoded_text_digraphs += huffman_codes_digraphs[digraph]
                    i += 2
                else:
                    encoded_text_digraphs += huffman_codes_chars[cleaned_text[i]]
                    i += 1
            if i < len(cleaned_text):
                encoded_text_digraphs += huffman_codes_chars[cleaned_text[i]]

            encoded_length_digraphs = len(encoded_text_digraphs)
            print(f"\nЗакодированный текст (первые 50 символов, Digraphs): {encoded_text_digraphs[:50]}...")
            print(f"Общая длина закодированного текста (Хаффман, Digraphs): {encoded_length_digraphs} бит")

            # --- Comparison with Uniform Encoding ---
            num_unique_chars = len(char_counts)
            uniform_code_length = math.ceil(math.log2(num_unique_chars))
            uniform_encoded_length = len(cleaned_text) * uniform_code_length
            print(f"\nДлина закодированного текста (равномерное {uniform_code_length}-битное кодирование): {uniform_encoded_length} бит")

            # --- Shannon Entropy Calculation ---
            entropy = shannon_entropy(char_counts, len(cleaned_text))
            print(f"\nЭнтропия Шеннона: {entropy:.4f} бит/символ\nОбщее количество информации: {entropy * len(cleaned_text):.4f} бит")

            # --- Сравнение с размером исходного текста ---
            print("\n--- Сравнение размеров ---")
            print(f"Размер исходного текста (UTF-8): {original_size} бит")
            print(f"Размер очищенного текста (UTF-8): {cleaned_size} бит")
            print(f"Коэффициент сжатия (Хаффман для символов): {cleaned_size / encoded_length_chars:.2f}x")
            print(f"Коэффициент сжатия (Хаффман для диграфов): {cleaned_size / encoded_length_digraphs:.2f}x")
            print(f"Коэффициент сжатия (равномерное кодирование): {cleaned_size / uniform_encoded_length:.2f}x")

    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Пример использования функции анализа текста
file_path = 'text_file.txt'
allowed_characters = 'abcdefghijklmnopqrstuvwxyz .,!?'
analyze_text(file_path, allowed_characters)
