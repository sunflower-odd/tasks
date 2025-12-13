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
    directions = [(-1,0),(1,0),(0,-1),(0,1)]

    for i in range(n):
        for j in range(m):
            if matrix[i][j] == 1 and not visited[i][j]:
                queue = deque()
                queue.append((i,j))
                visited[i][j] = True
                touches_border = False
                boundary_cells = set()

                while queue:
                    x, y = queue.popleft()
                    if x == 0 or y == 0 or x == n-1 or y == m-1:
                        touches_border = True
                    for dx, dy in directions:
                        nx, ny = x+dx, y+dy
                        if 0 <= nx < n and 0 <= ny < m:
                            if matrix[nx][ny] == 1 and not visited[nx][ny]:
                                visited[nx][ny] = True
                                queue.append((nx, ny))
                            elif matrix[nx][ny] == 0:
                                boundary_cells.add((nx, ny))

                # Если контур не касается границы и есть хотя бы один черный пиксель внутри → замкнут
                if not touches_border and boundary_cells:
                    return 'YES'
    return 'NO'

def func():
    matrix = read_matrix_from_file('input.txt')
    return has_closed_contour(matrix)

if __name__ == '__main__':
    print(func())