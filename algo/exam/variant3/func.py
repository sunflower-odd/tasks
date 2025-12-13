import re
import pprint
from fuzzywuzzy import fuzz

SIMILARITY_THRESHOLD = 0.8
USE_PREPROCESSING = True
WORDS_TO_EXCLUDE = ['смартфон', 'телефон', 'смарт', 'планшет','робот', 'пылесос', "новинка", "оригинал",
    "new", "original", "mobile"]

def clean_data(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()


        lines_list = []
        for line in lines:
            line = line.lower()
            line = re.sub(r"[^a-zа-я0-9\s]", " ", line)
            line = re.sub(r"\s+", " ", line).strip()
            line = re.sub(r"(\d+)\s*(gb|гб)", r"\1 gb", line)
            line = line.split()
            line = [t for t in line if t not in WORDS_TO_EXCLUDE]
            lines_list.append(line)

        lines_dict = {line[0]: line[1:] for line in lines_list}
        #print(lines_dict)
        return lines_dict


def tokenize(cleaned_dict):
    structured_dict = {
        item: {
            "numbers": sorted([t for t in item_values if t.isdigit()]),
            "words": sorted(set(t for t in item_values if not t.isdigit())),
        }
        for item, item_values in cleaned_dict.items()
    }
    #pprint.pprint(structured_dict)
    return structured_dict

def build_search_string(entry):
    tokens = list(entry['words']) + list(entry['numbers'])
    return " ".join(tokens)
def find_similar(query, search_index, threshold=SIMILARITY_THRESHOLD):
    results = []
    for item_id, text in search_index.items():
        print("Эту строку ищем: ", query)
        print("С этой строкой сравниваем: ", text)
        score = fuzz.token_set_ratio(query, text)
        print("Степень сходства: ", score)
        if score >= threshold*100:
            results.append({"catalog_id": item_id, "similarity_score": score})

    return results

if __name__ == '__main__':
    cleaned_dict_catalog = clean_data('catalog.txt')
    catalog_data = tokenize(cleaned_dict_catalog)

    cleaned_dict_new_items = clean_data('new_items.txt')
    new_items_data = tokenize(cleaned_dict_new_items)

    search_index = {item_id: build_search_string(data) for item_id, data in catalog_data.items()}
    final_results = {}
    for entry, entry_dict in new_items_data.items():
        search_string = build_search_string(entry_dict)
        results = find_similar(search_string, search_index, threshold=SIMILARITY_THRESHOLD)
        final_results[entry] = results

    print(final_results)




