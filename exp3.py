import random
random.seed(0)

def eval_cnf(assignment, cnf):
    sat = 0
    for clause in cnf:
        if any((assignment[v] ^ neg) for (v,neg) in clause):
            sat += 1
    return sat

def flip(assignment, idxs):
    a = assignment[:]
    for i in idxs: a[i] = not a[i]
    return a

def vnd(cnf, n_vars, max_iters=1000):
    # start with random assignment
    cur = [random.choice([True, False]) for _ in range(n_vars)]
    best = cur[:]
    best_val = eval_cnf(best, cnf)
    kmax = min(3, n_vars)  # neighborhoods of size 1..kmax
    iters = 0
    while iters < max_iters:
        improved = False
        k = 1
        while k <= kmax:
            improved_k = False
            # try flipping any k distinct variables (sampled)
            candidates = [tuple(sorted(random.sample(range(n_vars), k))) for _ in range(min(50, 1<<k * n_vars))]
            seen = set()
            for idxs in candidates:
                if idxs in seen: continue
                seen.add(idxs)
                new = flip(cur, idxs)
                val = eval_cnf(new, cnf)
                if val > best_val:
                    best, best_val = new, val
                    cur = new
                    improved = improved_k = True
                    break
            if improved_k:
                k = 1  # restart from smallest neighborhood
            else:
                k += 1
        iters += 1
        if not improved: break
    return best, best_val, len(cnf)

if __name__ == "__main__":
    # Example 3-SAT CNF with 4 vars (x0..x3)
    # (x0 ∨ ¬x1 ∨ x2) ∧ (¬x0 ∨ x1 ∨ x3) ∧ (x0 ∨ x2 ∨ ¬x3) ∧ (¬x2 ∨ x1 ∨ x3)
    cnf = [
        [(0,False),(1,True),(2,False)],
        [(0,True),(1,False),(3,False)],
        [(0,False),(2,False),(3,True)],
        [(2,True),(1,False),(3,False)],
    ]
    n_vars = 4
    assign, satisfied, total = vnd(cnf, n_vars, max_iters=200)
    print("Assignment:", assign)
    print(f"Satisfied {satisfied}/{total} clauses")
    print("Satisfiable?" , satisfied == total)
