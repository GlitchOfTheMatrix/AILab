import random
import time
import itertools

def parse_dimacs(filename):
    clauses = []
    num_vars = 0
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('c'):
                    continue
                if line.startswith('p cnf'):
                    parts = line.split()
                    num_vars = int(parts[2])
                elif line:
                    # Clause lines end with a 0, which we can ignore.
                    clause = [int(x) for x in line.split()[:-1]]
                    if clause:
                        clauses.append(clause)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return 0, []
    return num_vars, clauses

def evaluate(solution, clauses):
    unsatisfied_count = 0
    for clause in clauses:
        is_satisfied = False
        for literal in clause:
            var_index = abs(literal) - 1
            # Check if the literal's required value matches the solution's assignment
            if (literal > 0 and solution[var_index]) or \
               (literal < 0 and not solution[var_index]):
                is_satisfied = True
                break
        if not is_satisfied:
            unsatisfied_count += 1
    return unsatisfied_count

def find_best_neighbor_flip(solution, clauses, k):
    num_vars = len(solution)
    best_neighbor = list(solution)
    current_fitness = evaluate(solution, clauses)
    best_fitness = current_fitness

    # Generate all combinations of k indices to flip
    indices = range(num_vars)
    for flip_indices in itertools.combinations(indices, k):
        neighbor = list(solution)
        for i in flip_indices:
            neighbor[i] = not neighbor[i]
        
        neighbor_fitness = evaluate(neighbor, clauses)

        if neighbor_fitness < best_fitness:
            best_fitness = neighbor_fitness
            best_neighbor = neighbor
    
    return best_neighbor, best_fitness

def shake(solution, k):
    num_vars = len(solution)
    shaken_solution = list(solution)
    
    # Randomly choose k distinct indices to flip
    flip_indices = random.sample(range(num_vars), k)
    
    for i in flip_indices:
        shaken_solution[i] = not shaken_solution[i]
        
    return shaken_solution

def variable_neighborhood_descent(num_vars, clauses, max_iter=100, k_max=3, timeout_seconds=60):
    start_time = time.time()
    
    # 1. Generate a random initial solution
    current_solution = [random.choice([True, False]) for _ in range(num_vars)]
    best_solution = list(current_solution)
    best_fitness = evaluate(best_solution, clauses)

    print(f"Initial random solution has {best_fitness} unsatisfied clauses.")

    iteration = 0
    while iteration < max_iter and best_fitness > 0 and (time.time() - start_time) < timeout_seconds:
        iteration += 1
        k = 1
        
        # 2. Variable Neighborhood Search (Local Search Phase)
        local_optimum = list(current_solution)
        while k <= k_max:
            # Find the best neighbor in the k-flip neighborhood
            neighbor, neighbor_fitness = find_best_neighbor_flip(local_optimum, clauses, k)
            
            # If the neighbor is an improvement, move to it and restart search from k=1
            if neighbor_fitness < evaluate(local_optimum, clauses):
                local_optimum = neighbor
                print(f"  [Iter {iteration}, k={k}] Found improvement. New fitness: {neighbor_fitness}")
                k = 1 # Go back to the first neighborhood
            else:
                k += 1 # Try the next, larger neighborhood
        
        # Update global best if the local search found a better solution
        current_fitness = evaluate(local_optimum, clauses)
        if current_fitness < best_fitness:
            best_solution = list(local_optimum)
            best_fitness = current_fitness
            print(f"*** New global best found! Fitness: {best_fitness} ***")
            if best_fitness == 0:
                print("Perfect solution found!")
                break

        # 3. Shake Phase (to escape local optimum)
        # We shake the current best solution to find a new starting point
        current_solution = shake(best_solution, k_max)
        print(f"Iter {iteration}: Shaking solution. Starting next local search...")


    elapsed_time = time.time() - start_time
    print(f"\nSearch finished in {elapsed_time:.2f} seconds.")
    return best_solution, best_fitness


if __name__ == "__main__":
    # Create a dummy DIMACS file for demonstration
    cnf_content = """c This is a sample 3-SAT problem.
p cnf 5 3
1 -3 5 0
2 3 -4 0
-1 -2 4 0
"""
    filename = "sample.cnf"
    with open(filename, "w") as f:
        f.write(cnf_content)

    print(f"Solving 3-SAT problem from {filename}...")
    
    # Parse the file
    num_variables, sat_clauses = parse_dimacs(filename)
    
    if num_variables > 0:
        # Run the VND solver
        solution, unsatisfied = variable_neighborhood_descent(
            num_variables, 
            sat_clauses,
            max_iter=100,
            k_max=2 # Using k_max=2 for speed. 3 can be very slow for many variables.
        )
        
        print("\n--- Results ---")
        if unsatisfied == 0:
            print("SATISFIABLE: A valid assignment was found.")
        else:
            print("UNSATISFIABLE or solution not found in time. This is the best assignment found.")
        
        print(f"Unsatisfied clauses: {unsatisfied}")
        
        # Format solution for readability (Variable -> True/False)
        readable_solution = {i + 1: val for i, val in enumerate(solution)}
        print(f"Variable assignments: {readable_solution}")
