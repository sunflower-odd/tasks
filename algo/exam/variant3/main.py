import re
import config
import json

def _levenshtein_distance(a, b):
    """
    Принимает:
        a [str] - первая строка
        b [str] - вторая строка

    Вычисляет расстояния Левенштейна для a и b

    Возвращает:
        [int] - минимальное количество операций, необходимых, чтобы превратить одну строку в другую
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
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost
            )
    return dp[n][m]


def clean_data(file_name):
    """
    Принимает:
        file_name (str) — путь к текстовому файлу с данными по товарам.

	Если включена предобработка (config.USE_PREPROCESSING) делает очистку данных:
	- Переводит текст в нижний регистр.
	- Убирает все символы кроме букв, цифр и пробелов.
	- Приводит последовательные пробелы к одному пробелу.
	- Нормализует единицы памяти (50ГБ → 50 gb).
	- Делит строку на слова и числа.
	- Заменяет слова-синонимы на одно слово через config.COLOR_MAP.
	- Исключает слова, не помогающие идентификации товара, которые находятся в config.WORDS_TO_EXCLUDE.

    Если предобработка не включена - очистка данных не производится

    Возвращает:
        dict вида {item_id: [список токенов]}
    """
    lines_list = []
    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            if config.USE_PREPROCESSING:
                line = line.lower()
                line = re.sub(r"[^a-zа-я0-9\s]", " ", line)
                line = re.sub(r"\s+", " ", line).strip()
                line = re.sub(r"(\d+)\s*(gb|гб)", r"\1 gb", line)

                line = line.split()
                line = [config.COLOR_MAP.get(word, word) for word in line]
                line = [t for t in line if t not in config.WORDS_TO_EXCLUDE]
            else:
                line = line.split()
            lines_list.append(line)

        lines_dict = {line[0]: line[1:] for line in lines_list if line}
        return lines_dict


def tokenize(cleaned_dict):
    """
    Принимает:
        cleaned_dict (dict) — словарь, где ключ — ID товара, значение — список токенов.

    Приводит очищенные данные к формату словаря с отдельно токенами-числами и отдельно текстовыми токенами

    Возвращает:
        structured_dict (dict) - словарь вида:
        {
            "my_id": {
                "numbers": ["..."],
                "words": ["..."]
            },
                ...
        }
    """
    structured_dict = {
        item: {
            "numbers": sorted([t for t in item_values if t.isdigit()]),
            "words": sorted(set(t for t in item_values if not t.isdigit())),
        }
        for item, item_values in cleaned_dict.items()
    }
    return structured_dict

def build_search_string(entry):
    """ Приводит одну единицу товара в формат токена, где данные очищены и отсортированы в едином порядке """
    return ' '.join(entry['words'] + entry['numbers'])

def find_similar(query, search_index, threshold=config.SIMILARITY_THRESHOLD):
    """
    Принимает:
        query (str) — строка, для которой ищем похожие товары.
	    search_index (dict) — словарь всех товаров из каталога с готовыми поисковыми строками (item_id: search_string).
	    threshold (float) — порог схожести (0–1), выше которого товар считается дубликатом.

    Ищет похожие товары:
    - Перебирает все товары в search_index.
	- Вычисляет расстояние Левенштейна между query и каждым товаром.
    - Вычисляет степень схожести

    Возвращает:
        list - данные с найденными дубликатами в заданном формате
    """
    results = []
    for item_id, text in search_index.items():
        levenshtein_dist = _levenshtein_distance(query, text)
        similarity = 1 - levenshtein_dist / max(len(query), len(text))
        if similarity >= threshold:
            results.append({"catalog_id": item_id, "similarity_score": similarity})

    return results

def main(new_items_file_name, catalog_file_name):
    """
    Получает данные на вход
	Записывает результаты в duplicates.json в заданном формате.
    """
    cleaned_dict_catalog = clean_data(catalog_file_name)
    catalog_data = tokenize(cleaned_dict_catalog)

    cleaned_dict_new_items = clean_data(new_items_file_name)
    new_items_data = tokenize(cleaned_dict_new_items)

    search_index = {item_id: build_search_string(data) for item_id, data in catalog_data.items()}
    final_results = {}
    for entry, entry_dict in new_items_data.items():
        search_string = build_search_string(entry_dict)
        results = find_similar(search_string, search_index, threshold=config.SIMILARITY_THRESHOLD)
        final_results[entry] = results

    with open("duplicates.json", "w", encoding="utf-8") as f:
        json.dump(final_results, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main(new_items_file_name=config.NEW_ITEMS_FILE_NAME, catalog_file_name=config.CATALOG_FILE_NAME)