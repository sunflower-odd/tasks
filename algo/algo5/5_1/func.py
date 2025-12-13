import math

def dist_circle(point, circle):
    # circle = ('circle', xc, yc, r)
    _, xc, yc, r = circle
    return math.dist(point, (xc, yc)) - r


def dist_point_to_segment(px, py, x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    if dx == 0 and dy == 0:
        return math.hypot(px - x1, py - y1)

    t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)
    t = max(0, min(1, t))

    proj_x = x1 + t * dx
    proj_y = y1 + t * dy

    return math.hypot(px - proj_x, py - proj_y)


def dist_to_polygon(point, polygon):
    # polygon = ('polygon', [(x1,y1),...,])
    _, points = polygon
    x0, y0 = point

    best = float("inf")
    m = len(points)

    for i in range(m):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % m]
        d = dist_point_to_segment(x0, y0, x1, y1, x2, y2)
        best = min(best, d)

    return best


def func():
    with open('input.txt', 'r') as f:
        lines = f.readlines()

        my_point = tuple(map(float, lines[0].split()))
        n = int(lines[1])

        shapes = []
        idx = 2

        for num in range(n):
            parts = lines[idx].split()
            idx += 1

            if parts[0] == "Circle":
                xc, yc, r = map(float, parts[1:])
                shapes.append(("circle", xc, yc, r))

            elif parts[0] == "Polygon":
                m = int(parts[1])
                coords = list(map(float, parts[2:2 + 2 * m]))
                pts = [(coords[i], coords[i + 1]) for i in range(0, 2 * m, 2)]
                shapes.append(("polygon", pts))

    distances = []
    for shape in shapes:
        if shape[0] == "circle":
            distances.append(dist_circle(my_point, shape))
        else:
            distances.append(dist_to_polygon(my_point, shape))

    #print("Shapes:", shapes)
    min_value = distances.index(min(distances))+1
    return min_value

print(func())



if __name__ == '__main__':
    func()