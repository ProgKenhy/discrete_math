import math

unique = ['Ч', 'Р', 'П', 'Л', 'И', 'Ц', 'А']  # 7 уникальных букв
repeating = ['Е', 'С', 'О']  # 3 буквы с повторениями

# Случай 1: Все 4 буквы уникальны
case1 = math.comb(10, 4) * math.factorial(4)  # 5040

# Случай 2: Одна буква повторяется 2 раза + 2 уникальные
case2 = 0
for r in repeating:
    remaining = unique + [x for x in repeating if x != r]  # 9 букв
    combinations_uniq = math.comb(9, 2)  # C(9,2) = 36
    permutations = math.factorial(4) // 2  # 12
    case2 += combinations_uniq * permutations  # 432 на каждую букву

# Случай 3: Две пары повторяющихся
case3 = math.comb(3, 2) * (math.factorial(3))  # 18

total = case1 + case2 + case3
print(f"Правильный ответ: {total}")  # 5040 + 1296 + 18 = 6354