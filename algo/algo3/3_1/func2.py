def prefix_function(sample):
    m = len(sample)

    pi = [0] * m
    k = 0

    for q in range(1, m):
        j = pi[q-1]
        while k > 0 and sample[q] != sample[j]:
            k = pi[k - 1]
        if sample[k] == sample[q]:
            k = k+1
        pi[q] = k
    return pi

def levenshtein_distance(a, b):
    """
    # Функция для вычисления расстояния Левенштейна
    """
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                cost = 0
            else:
                cost = 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,  # удаление
                dp[i][j - 1] + 1,  # вставка
                dp[i - 1][j - 1] + cost  # замена
            )
    return dp[n][m]


def func():
    import re
    with open("input.txt", 'r') as f:
        content = f.readline().strip()
        k = int(f.readline().strip())
        #content_list = content.split()
        content_list = re.findall(r'\b\w+\b', content.lower())

    # Считаем префикс-функцию для каждого слова
    pi_dict = {word: sum(prefix_function(word)) for word in content_list}

    # Находим слово с максимальной суммой префикс-функции
    max_pi_value = max(pi_dict.values())
    max_keys = {w for w, v in pi_dict.items() if v == max_pi_value}

    # Если несколько слов — выбираем самое длинное, если несколько — сортируем и берём первое
    if len(max_keys) == 1:
        max_pi_word = next(iter(max_keys))
    else:
        max_len = max(len(word) for word in max_keys)
        longest_words = [word for word in max_keys if len(word) == max_len]

        max_pi_word, earliest_index = min(
            (
                (word, i)
                for i, word in enumerate(content_list)
                if word in longest_words
            ),
            key=lambda x: x[1]
        )

    # Считаем количество слов, отличающихся не более чем на k по Левенштейну
    content_set = set(content_list)

    count_similar = sum(
        1 for word in content_set
        if word != max_pi_word and levenshtein_distance(word, max_pi_word) <= k
    )


    print(max_pi_word)
    print(max_pi_value)
    print(count_similar)


if __name__ == "__main__":
    func()