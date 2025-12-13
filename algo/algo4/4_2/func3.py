def min_points_to_cover_intervals():
    with open('input.txt', 'r') as f:
        lines = f.readlines()
        i = 0
        intervals = []
        for line in lines:
            if i==0:
                n=int(line[0])
                i=i+1

            else:
                item =list(map(int, line.split()))
                intervals.append(item)


    # Сортируем отрезки по концу
    intervals.sort(key=lambda x: x[1])

    points = []
    while intervals:
        # Берём конец первого отрезка как точку контроля
        point = intervals[0][1]
        points.append(point)

        # Убираем все отрезки, которые покрывает эта точка
        intervals = [iv for iv in intervals if iv[0] > point]

    print(points)


if __name__ == "__main__":
    min_points_to_cover_intervals()