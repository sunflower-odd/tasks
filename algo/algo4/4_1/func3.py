def func():
    with open('input.txt', 'r') as f:
        lines = f.readlines()
        i = 0
        for line in lines:
            if i==0:
                W=int(line)
                i+=1
            elif i==1:
                n=int(line)
                i += 1
            else:
                weights = list(map(int, line.split()))
                weights.sort(reverse=True)

    bits = 1

    for w in weights:
        bits |= bits << w
        bits &= (1 << (W + 1)) - 1

    for ans in range(W, -1, -1):
        if (bits >> ans) & 1:
            print(ans)
            break

if __name__ == '__main__':
    func()