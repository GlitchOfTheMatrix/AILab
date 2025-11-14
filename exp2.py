# 8-Puzzle using DFID (Iterative Deepening DFS)
GOAL = (1,2,3,4,5,6,7,8,0)

def is_solvable(state):
    arr = [x for x in state if x != 0]
    inv = sum(arr[i] > arr[j] for i in range(len(arr)) for j in range(i+1, len(arr)))
    return inv % 2 == 0

def neighbors(state):
    idx = state.index(0)
    r, c = divmod(idx, 3)
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = r+dr, c+dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            nidx = nr*3+nc
            s = list(state)
            s[idx], s[nidx] = s[nidx], s[idx]
            yield tuple(s)

def dls(node, depth, visited):
    if node == GOAL: return [node]
    if depth == 0: return None
    visited.add(node)
    for nb in neighbors(node):
        if nb not in visited:
            res = dls(nb, depth-1, visited)
            if res is not None:
                return [node] + res
    visited.remove(node)
    return None

def iddfs(start, max_depth=40):
    if start == GOAL: return [start]
    if not is_solvable(start): return None
    for depth in range(max_depth+1):
        visited = set()
        res = dls(start, depth, visited)
        if res is not None:
            return res
    return None

if __name__ == "__main__":
    start = (1,2,3,4,5,6,0,7,8)
    path = iddfs(start)
    if path is None:
        print("Unsolvable or depth limit exceeded.")
    else:
        print("Depth:", len(path)-1)
        for i, st in enumerate(path):
            print(f"Step {i}:")
            for r in range(0,9,3):
                print(st[r:r+3])
