def max_gold_weight():
    with open('input.txt', 'r') as f:
        lines = f.readlines()
        W = int(lines[0])
        n = int(lines[1])
        weights = list(map(int, lines[2].split()))

    dp = [False] * (W + 1)
    dp[0] = True

    for w in weights:
        for s in range(W, w - 1, -1):
            if dp[s - w]:
                dp[s] = True

    for wgt in range(W, -1, -1):
        if dp[wgt]:
            print(wgt)
            break

if __name__ == '__main__':
    max_gold_weight()