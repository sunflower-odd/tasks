def func():
    with open('input.txt', 'r') as f:
        lines = f.readlines()
        i = 0
        segments = []
        for line in lines:
            if i==0:
                n=int(line[0])
                i=i+1

            else:
                item =list(map(int, line.split()))
                segments.append(item)

    segments.sort(key=lambda x: x[0])
    num = 1
    for i in range(len(segments)-1):
        for j in range(len(segments)-1):
            if segments[j+1][0]>segments[i][1]:
                print(f'segments[j+1][0]: {segments[j+1][0]}, segments[i][1]: {segments[i][1]} ')
                num=num+1
                break

    print(num)




if __name__ == '__main__':
    func()