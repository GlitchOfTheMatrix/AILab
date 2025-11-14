# 8-Puzzle using Generate and Test (BFS)
from collections import deque

GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)

def is_solvable(state):
    arr = [x for x in state if x != 0]
    inv = sum(arr[i] > arr[j] for i in range(len(arr)) for j in range(i + 1, len(arr)))
    return inv % 2 == 0

def neighbors(state):
    idx = state.index(0)
    r, c = divmod(idx, 3)
    moves = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            nidx = nr * 3 + nc
            s = list(state)
            s[idx], s[nidx] = s[nidx], s[idx]
            moves.append(tuple(s))
    return moves

def bfs(start):
    if start == GOAL:
        return [start]
    if not is_solvable(start):
        return None

    q = deque([start])
    parent = {start: None}

    while q:
        cur = q.popleft()
        if cur == GOAL:
            path = []
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            return path[::-1]
        for nb in neighbors(cur):
            if nb not in parent:
                parent[nb] = cur
                q.append(nb)
    return None

if __name__ == "__main__":
    start = (1, 2, 3,
             4, 5, 6,
             0, 7, 8)
    path = bfs(start)
    if path is None:
        print("Unsolvable or no path found.")
    else:
        print("Moves:", len(path) - 1)
        for i, st in enumerate(path):
            print(f"Step {i}:")
            for r in range(0, 9, 3):
                print(st[r:r + 3])
