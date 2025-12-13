import re
import config
import json

def levenshtein_distance(a, b):
    """ Вычисление расстояния Левенштейна"""
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
    """Очищаем данные"""
    with open(file_name, 'r') as f:
        lines = f.readlines()

    lines_list = []
    for line in lines:
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
    """ Приводим очищенные данные к формату словаря с отдельно токенами-числами и отдельно текстовыми токенами """
    structured_dict = {
        item: {
            "numbers": sorted([t for t in item_values if t.isdigit()]),
            "words": sorted(set(t for t in item_values if not t.isdigit())),
        }
        for item, item_values in cleaned_dict.items()
    }
    return structured_dict

def build_search_string(entry):
    """ Приводим одну единицу товара в формат токена, где данные очищены и отсортированы в едином порядке """
    tokens = list(entry['words']) + list(entry['numbers'])
    return " ".join(tokens)

def find_similar(query, search_index, threshold=config.SIMILARITY_THRESHOLD):
    results = []
    for item_id, text in search_index.items():
        print("Эту строку ищем: ", query)
        print("С этой строкой сравниваем: ", text)
        levenshtein_dist = levenshtein_distance(query, text)
        print("Расстояние Левенштейна: ", levenshtein_dist)
        similarity = 1 - levenshtein_dist / max(len(query), len(text))
        print("Степень сходства: ", similarity)
        if similarity >= threshold:
            results.append({"catalog_id": item_id, "similarity_score": similarity})

    return results

def main():
    cleaned_dict_catalog = clean_data('catalog.txt')
    catalog_data = tokenize(cleaned_dict_catalog)

    cleaned_dict_new_items = clean_data('new_items.txt')
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
    main()