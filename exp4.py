# 3-SAT using Stochastic Hill Climbing with random restarts
import random
random.seed(1)

def eval_cnf(assignment, cnf):
    sat = 0
    for clause in cnf:
        if any((assignment[v] ^ neg) for (v,neg) in clause):
            sat += 1
    return sat

def hill_climb(cnf, n_vars, max_steps=500, p_sideways=0.1):
    best_assign = None
    best_val = -1
    for _ in range(50):  # restarts
        cur = [random.choice([True, False]) for _ in range(n_vars)]
        cur_val = eval_cnf(cur, cnf)
        for _ in range(max_steps):
            improved = False
            cand_idxs = list(range(n_vars))
            random.shuffle(cand_idxs)
            for i in cand_idxs:
                new = cur[:]
                new[i] = not new[i]
                val = eval_cnf(new, cnf)
                if val > cur_val or (val == cur_val and random.random() < p_sideways):
                    cur, cur_val = new, val
                    improved = True
                    break
            if not improved:
                break
        if cur_val > best_val:
            best_assign, best_val = cur, cur_val
        if best_val == len(cnf):
            break
    return best_assign, best_val, len(cnf)

if __name__ == "__main__":
    cnf = [
        [(0,False),(1,True),(2,False)],
        [(0,True),(1,False),(3,False)],
        [(0,False),(2,False),(3,True)],
        [(2,True),(1,False),(3,False)],
    ]
    n_vars = 4
    assign, satisfied, total = hill_climb(cnf, n_vars)
    print("Assignment:", assign)
    print(f"Satisfied {satisfied}/{total} clauses")
    print("Satisfiable?" , satisfied == total)
