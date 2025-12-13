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
    print(segments)
    num = 1
    segments.sort(key=lambda x: (x[0], x[1]))

    final_list = []

    while segments:
        base = segments[0]
        group = [base]
        segments.pop(0)

        i = 0
        while i < len(segments):
            print(f'segments[i][0] {segments[i]}, base[1]: {base} ')
            if segments[i][0] <= base[1]:
                for group_segment in group:
                    if group_segment[0]<=base[1]:
                        group.append(segments[i])
                        segments.pop(i)
            else:
                i += 1

        final_list.append(group)
        segments = [item for item in segments if item not in group]


    print(final_list)
    final_list = [sub for sub in final_list if sub]
    print(final_list)
    print(len(final_list))




if __name__ == '__main__':
    func()