from collections import deque

def read_matrix_from_file(filename):
    matrix = []
    with open(filename, 'r') as f:
        for line in f:
            row = list(map(int, line.strip().split()))
            matrix.append(row)
    return matrix

def has_closed_white_contour(matrix):
    n, m = len(matrix), len(matrix[0])
    visited = [[False]*m for _ in range(n)]
    directions = [(-1,0),(1,0),(0,-1),(0,1)]

    for i in range(n):
        for j in range(m):
            if matrix[i][j] == 0 and not visited[i][j]:
                queue = deque()
                queue.append((i,j))
                visited[i][j] = True
                touches_border = False

                while queue:
                    x, y = queue.popleft()
                    if x==0 or y==0 or x==n-1 or y==m-1:
                        touches_border = True
                    for dx,dy in directions:
                        nx, ny = x+dx, y+dy
                        if 0<=nx<n and 0<=ny<m:
                            if matrix[nx][ny]==0 and not visited[nx][ny]:
                                visited[nx][ny]=True
                                queue.append((nx,ny))

                if not touches_border:
                    # Черная область полностью окружена белым → есть замкнутый белый контур
                    return 'YES'
    return 'NO'

if __name__=='__main__':
    matrix = read_matrix_from_file('input2.txt')
    print(has_closed_white_contour(matrix))