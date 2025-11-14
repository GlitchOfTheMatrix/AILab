# 8-Puzzle A* (Manhattan distance)
import heapq

GOAL = (1,2,3,4,5,6,7,8,0)
goal_pos = {v:i for i,v in enumerate(GOAL)}

def is_solvable(state):
    arr = [x for x in state if x != 0]
    inv = sum(arr[i] > arr[j] for i in range(len(arr)) for j in range(i+1, len(arr)))
    return inv % 2 == 0

def manhattan(state):
    dist = 0
    for i, v in enumerate(state):
        if v == 0: continue
        gi = goal_pos[v]
        r1,c1 = divmod(i,3)
        r2,c2 = divmod(gi,3)
        dist += abs(r1-r2)+abs(c1-c2)
    return dist

def neighbors(state):
    idx = state.index(0)
    r,c = divmod(idx,3)
    for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr,nc = r+dr,c+dc
        if 0<=nr<3 and 0<=nc<3:
            nidx = nr*3+nc
            s = list(state)
            s[idx], s[nidx] = s[nidx], s[idx]
            yield tuple(s)

def astar(start):
    if start == GOAL: return [start]
    if not is_solvable(start): return None
    openh = []
    g = {start:0}
    parent = {start:None}
    heapq.heappush(openh, (manhattan(start), 0, start))
    closed = set()
    while openh:
        f, gc, cur = heapq.heappop(openh)
        if cur in closed: continue
        closed.add(cur)
        if cur == GOAL:
            path = []
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            return path[::-1]
        for nb in neighbors(cur):
            ng = g[cur] + 1
            if nb not in g or ng < g[nb]:
                g[nb] = ng
                parent[nb] = cur
                heapq.heappush(openh, (ng + manhattan(nb), ng, nb))
    return None

if __name__ == "__main__":
    start = (1,2,3,4,5,6,0,7,8)
    path = astar(start)
    if path is None:
        print("Unsolvable.")
    else:
        print("Optimal moves:", len(path)-1)
        for i, st in enumerate(path):
            print(f"Step {i}:")
            for r in range(0,9,3):
                print(st[r:r+3])
