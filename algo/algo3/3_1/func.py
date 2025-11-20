
def prefix_function(s):
    n = len(s)
    pi = [0] * n
    for i in range(1, n):
        j = pi[i-1]
        while j > 0 and s[i] != s[j]:
            j = pi[j-1]
        if s[i] == s[j]:
            j += 1
        pi[i] = j
    return pi

def func():
    with open("input.txt", 'r') as f:
        content = f.readline()
        k = f.readline()
        content_list = content.split(" ")
        print(content_list)
        pi_dict = {}
        for word in content_list:
            pi_dict[word] = sum(prefix_function(word))

        max_pi_value = max(pi_dict.values())
        max_keys = [k for k, v in pi_dict.items() if v == max_pi_value]
        if len(max_keys) == 1:
            max_pi_word = max_keys[0]
        else:
            max_len = max(len(word) for word in max_keys)
            longest_words = [word for word in max_keys if len(word) == max_len]
            if len(longest_words)==1:
                max_pi_word = longest_words[0]
            else:
                longest_words.sort()
                max_pi_word = longest_words[0]




if __name__ == "__main__":
    func()