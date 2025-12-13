def func():
    # Чтение данных
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    n = int(lines[0].strip())  # количество сегментов, если нужно
    segments = [list(map(int, line.split())) for line in lines[1:]]

    # Сортировка по началу сегмента
    segments.sort(key=lambda x: x[0])

    final_list = []

    while segments:
        base = segments[0]
        group = [base]
        segments.pop(0)

        # Формируем новую версию списка сегментов без элементов, которые добавили в группу
        remaining_segments = []
        for seg in segments:
            if seg[0] <= base[1]:  # если пересекается с базовым сегментом
                group.append(seg)
                base[1] = max(base[1], seg[1])  # расширяем границу объединённого сегмента
            else:
                remaining_segments.append(seg)

        segments = remaining_segments
        final_list.append(group)

    # Вывод результата
    print(final_list)
    print(len(final_list))


if __name__ == '__main__':
    func()