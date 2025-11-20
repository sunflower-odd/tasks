def decode(encoded, reverse_codes):
    decoded = ''
    current_code = ''
    #reverse_codes = {}
    for bit in encoded:
        current_code = current_code+bit
        if current_code in reverse_codes:
            decoded = decoded+reverse_codes[current_code]
            current_code=''

    if current_code:
        raise RuntimeError("Invalid encoded string")

    return decoded

def max_unique_split(s):
    max_count = 0

    def backtrack(start, used):
        nonlocal max_count
        if start == len(s):
            max_count = max(max_count, len(used))
            return
        for end in range(start + 1, len(s) + 1):
            substring = s[start:end]
            if substring not in used:
                used.add(substring)
                backtrack(end, used)
                used.remove(substring)

    backtrack(0, set())
    return max_count

def main():
    import re
    with open('input.txt', 'r') as f:
        alphabet_count = int(f.readline().strip())

        lines = {}
        for i in range(alphabet_count):
            line_name = f"line{i + 1}"
            lines[line_name] = f.readline().strip()

        encoded_string = f.readline().strip()
        reverse_codes = {}
        for line_name in lines:
            codes_list = re.findall(r'\b\w+\b', lines[line_name])
            if len(codes_list) >= 2:
                reverse_codes[codes_list[1]] = codes_list[0]

        decoded_text = decode(encoded_string, reverse_codes)
        print(decoded_text)

        max_unique_pairs_count = max_unique_split(decoded_text)
        print(max_unique_pairs_count)



if __name__ == "__main__":
    main()
