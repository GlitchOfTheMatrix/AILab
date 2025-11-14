import heapq
import itertools

# The goal state for the 8-puzzle
GOAL_STATE = ((1, 2, 3), (4, 5, 6), (7, 8, 0))

def calculate_manhattan_distance(board):
    """
    Calculates the Manhattan distance heuristic for a given board state.
    The distance is the sum of the Manhattan distances of each tile
    from its goal position.
    """
    distance = 0
    for r in range(3):
        for c in range(3):
            value = board[r][c]
            if value != 0:
                # Goal position for the value
                goal_r, goal_c = (value - 1) // 3, (value - 1) % 3
                distance += abs(r - goal_r) + abs(c - goal_c)
    return distance

def find_empty_tile(board):
    """Finds the (row, col) of the empty tile (0)."""
    for r, row in enumerate(board):
        for c, value in enumerate(row):
            if value == 0:
                return r, c
    return None # Should not happen on a valid board

def get_neighbors(board):
    """Generates all valid neighbor states from the current state."""
    neighbors = []
    empty_r, empty_c = find_empty_tile(board)

    # Possible moves: Up, Down, Left, Right
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_r, new_c = empty_r + dr, empty_c + dc

        if 0 <= new_r < 3 and 0 <= new_c < 3:
            # Create a mutable copy to perform the swap
            new_board_list = [list(row) for row in board]
            new_board_list[empty_r][empty_c], new_board_list[new_r][new_c] = \
                new_board_list[new_r][new_c], new_board_list[empty_r][empty_c]
            
            # Convert back to a tuple of tuples to be hashable
            new_board = tuple(tuple(row) for row in new_board_list)
            neighbors.append(new_board)
            
    return neighbors

def is_solvable(board):
    """
    Checks if the 8-puzzle is solvable.
    A puzzle is solvable if the number of inversions is even.
    An inversion is any pair of tiles that are in the wrong order.
    """
    # Flatten the board into a 1D list, ignoring the empty tile
    flat_board = [tile for tile in itertools.chain(*board) if tile != 0]
    inversions = 0
    for i in range(len(flat_board)):
        for j in range(i + 1, len(flat_board)):
            if flat_board[i] > flat_board[j]:
                inversions += 1
    return inversions % 2 == 0

def solve_puzzle(initial_board):
    """
    Solves the 8-puzzle using Greedy Best-First Search.
    The priority queue stores tuples of (heuristic, board_state, path).
    """
    # Convert initial board to tuple of tuples to be hashable
    initial_board = tuple(tuple(row) for row in initial_board)

    if not is_solvable(initial_board):
        print("The initial configuration is not solvable.")
        return None

    # Priority queue: (heuristic_cost, current_board, path_to_current)
    priority_queue = []
    initial_h = calculate_manhattan_distance(initial_board)
    heapq.heappush(priority_queue, (initial_h, initial_board, [initial_board]))

    # A set to keep track of visited states to avoid cycles
    visited = set()

    while priority_queue:
        h, current_board, path = heapq.heappop(priority_queue)

        if current_board == GOAL_STATE:
            return path

        if current_board in visited:
            continue

        visited.add(current_board)

        for neighbor in get_neighbors(current_board):
            if neighbor not in visited:
                neighbor_h = calculate_manhattan_distance(neighbor)
                new_path = path + [neighbor]
                heapq.heappush(priority_queue, (neighbor_h, neighbor, new_path))

    return None  # No solution found

def print_board(board):
    """Helper function to print a board state nicely."""
    for row in board:
        print(" ".join(map(str, row)).replace('0', '_'))

if __name__ == "__main__":
    # Example initial state (must be solvable)
    initial_board = [
        [1, 2, 3],
        [0, 4, 6],
        [7, 5, 8]
    ]

    # Another example:
    # initial_board = [
    #     [8, 1, 2],
    #     [0, 4, 3],
    #     [7, 6, 5]
    # ]

    print("Solving 8-puzzle with Best-First Search...")
    print("Initial State:")
    print_board(initial_board)
    print("-" * 20)

    solution_path = solve_puzzle(initial_board)

    if solution_path:
        print(f"Goal state reached in {len(solution_path) - 1} moves!")
        print("Path from start to goal:")
        for i, board in enumerate(solution_path):
            print(f"\nStep {i}:")
            print_board(board)
    else:
        print("Could not find a solution.")
