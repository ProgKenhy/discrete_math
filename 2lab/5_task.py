import math
from functools import lru_cache

# Задача 1: Без ограничений
def count_paths(m, n):
    return math.comb(m + n, m)

m, n = 18, 16
print(f"Количество путей без ограничений: {count_paths(m, n)}")

# Задача 2: с ограничениями
def count_paths_recursive(m: int, n: int) -> int:
    @lru_cache(maxsize=None)
    def dfs(x, y, last_is_up):
        """
        x, y: текущие координаты
        last_is_up: True, если последний шаг был вертикальным (вверх)
        """
        # Дошли до цели
        if x == m and y == n:
            return 1

        total = 0

        # Шаг вправо (если возможно)
        if x < m:
            total += dfs(x + 1, y, False)

        # Шаг вверх (если разрешено и возможно)
        if y < n and not last_is_up:
            total += dfs(x, y + 1, True)

        return total

    # Начинаем из точки (0, 0), last_is_up=False (первый шаг может быть любым)
    return dfs(0, 0, False)


result = count_paths_recursive(m, n)
print(f"Количество путей с ограничением (рекурсия): {result}")
