import random
import time

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
            if (literal > 0 and solution[var_index]) or \
               (literal < 0 and not solution[var_index]):
                is_satisfied = True
                break
        if not is_satisfied:
            unsatisfied_count += 1
    return unsatisfied_count

def stochastic_hill_climbing(num_vars, clauses, max_restarts=50, max_steps=1000):
    start_time = time.time()
    best_solution_so_far = []
    best_fitness_so_far = float('inf')

    for restart in range(max_restarts):
        # 1. Start with a random solution
        current_solution = [random.choice([True, False]) for _ in range(num_vars)]
        
        # Keep track of the best solution for this specific run
        if not best_solution_so_far:
            best_solution_so_far = list(current_solution)
            best_fitness_so_far = evaluate(current_solution, clauses)

        print(f"\n[Restart #{restart + 1}] Starting with a new random solution. Initial unsatisfied: {evaluate(current_solution, clauses)}")

        for step in range(max_steps):
            current_fitness = evaluate(current_solution, clauses)

            # If a perfect solution is found, we're done
            if current_fitness == 0:
                print(">>> Perfect solution found! <<<")
                return current_solution, 0

            # 2. Find all neighbors that are an improvement
            improving_neighbors = []
            for i in range(num_vars):
                # Create a neighbor by flipping the i-th variable
                neighbor_solution = list(current_solution)
                neighbor_solution[i] = not neighbor_solution[i]
                
                neighbor_fitness = evaluate(neighbor_solution, clauses)

                if neighbor_fitness < current_fitness:
                    improving_neighbors.append((neighbor_solution, neighbor_fitness))

            # 3. Choose the next move
            if not improving_neighbors:
                # If no neighbor is better, we're stuck at a local optimum. Break to restart.
                print(f"  Stuck at a local optimum with {current_fitness} unsatisfied clauses. Restarting...")
                break
            
            # STOCHASTIC step: Randomly choose from the list of better options
            chosen_neighbor, chosen_fitness = random.choice(improving_neighbors)
            current_solution = chosen_neighbor
            
            # Update the best-ever solution if this step is an improvement
            if chosen_fitness < best_fitness_so_far:
                best_fitness_so_far = chosen_fitness
                best_solution_so_far = list(current_solution)
                print(f"  Step {step+1}: New best fitness found: {best_fitness_so_far}")

        # Check if this restart found a better solution than previous restarts
        final_run_fitness = evaluate(current_solution, clauses)
        if final_run_fitness < best_fitness_so_far:
            best_fitness_so_far = final_run_fitness
            best_solution_so_far = list(current_solution)

    elapsed_time = time.time() - start_time
    print(f"\nSearch finished in {elapsed_time:.2f} seconds.")
    return best_solution_so_far, best_fitness_so_far

if __name__ == "__main__":
    # Create a dummy DIMACS file for demonstration
    cnf_content = """c This is a sample 3-SAT problem.
p cnf 20 15
1 -5 4 0
-1 5 3 0
-3 -4 2 0
-2 18 -12 0
11 15 20 0
-11 -15 -20 0
1 15 -20 0
-1 -15 20 0
5 11 20 0
-5 -11 -20 0
4 11 15 0
-4 -11 -15 0
2 8 9 0
-13 14 -16 0
17 -19 7 0
"""
    filename = "sample.cnf"
    with open(filename, "w") as f:
        f.write(cnf_content)

    print(f"Solving 3-SAT problem from {filename}...")
    
    num_variables, sat_clauses = parse_dimacs(filename)
    
    if num_variables > 0:
        solution, unsatisfied = stochastic_hill_climbing(
            num_variables, 
            sat_clauses,
            max_restarts=20,
            max_steps=500
        )
        
        print("\n--- Results ---")
        if unsatisfied == 0:
            print("SATISFIABLE: A valid assignment was found.")
        else:
            print("UNSATISFIABLE or solution not found in time. This is the best assignment found.")
        
        print(f"Unsatisfied clauses: {unsatisfied}")
        readable_solution = {i + 1: val for i, val in enumerate(solution)}
        print(f"Best variable assignments found: {readable_solution}")
