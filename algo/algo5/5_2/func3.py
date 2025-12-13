from collections import deque

def read_matrix_from_file(filename):
    matrix = []
    with open(filename, 'r') as f:
        for line in f:
            row = list(map(int, line.strip().split()))
            matrix.append(row)
    return matrix

def has_closed_contour(matrix):
    n, m = len(matrix), len(matrix[0])
    visited = [[False] * m for _ in range(n)]
    # 8 направлений: вертикаль, горизонталь, диагонали
    directions = [(-1,0),(1,0),(0,-1),(0,1), (-1,-1), (-1,1), (1,-1), (1,1)]

    # Запускаем BFS от всех нулей на границе
    queue = deque()
    for i in range(n):
        for j in [0, m-1]:
            if matrix[i][j] == 0 and not visited[i][j]:
                queue.append((i,j))
                visited[i][j] = True
    for j in range(m):
        for i in [0, n-1]:
            if matrix[i][j] == 0 and not visited[i][j]:
                queue.append((i,j))
                visited[i][j] = True

    while queue:
        x, y = queue.popleft()
        for dx, dy in directions:
            nx, ny = x+dx, y+dy
            if 0 <= nx < n and 0 <= ny < m and matrix[nx][ny] == 0 and not visited[nx][ny]:
                visited[nx][ny] = True
                queue.append((nx, ny))

    # Если есть нули, которые мы не достигли с границы → замкнутый контур
    for i in range(n):
        for j in range(m):
            if matrix[i][j] == 0 and not visited[i][j]:
                return "YES"

    return "NO"

def func():
    matrix = read_matrix_from_file('input.txt')
    return has_closed_contour(matrix)

if __name__ == '__main__':
    print(func())