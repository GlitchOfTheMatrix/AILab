# Simple 8-Puzzle solver using DFID (Depth First Iterative Deepening)
# The puzzle is a 3x3 grid. 0 is the blank space.

def is_goal(state):
	return state == [1,2,3,4,5,6,7,8,0]

def get_moves(pos):
	moves = []
	row, col = pos // 3, pos % 3
	if row > 0: moves.append(pos - 3)      # Up
	if row < 2: moves.append(pos + 3)      # Down
	if col > 0: moves.append(pos - 1)      # Left
	if col < 2: moves.append(pos + 1)      # Right
	return moves

def dls(state, depth, limit, path, visited):
	if is_goal(state):
		return path
	if depth == limit:
		return None
	visited.add(tuple(state))
	zero_pos = state.index(0)
	for move in get_moves(zero_pos):
		new_state = state[:]
		new_state[zero_pos], new_state[move] = new_state[move], new_state[zero_pos]
		if tuple(new_state) in visited:
			continue
		move_name = ["Up", "Down", "Left", "Right"][[move == zero_pos - 3, move == zero_pos + 3, move == zero_pos - 1, move == zero_pos + 1].index(True)]
		result = dls(new_state, depth + 1, limit, path + [move_name], visited)
		if result:
			return result
	visited.remove(tuple(state))
	return None

def dfid(start_state, max_depth=20):
	for limit in range(max_depth + 1):
		visited = set()
		result = dls(start_state, 0, limit, [], visited)
		if result:
			return result
	return None

def main():
	print("Enter the initial 8-puzzle state as 9 numbers (use 0 for blank):")
	state = []
	for _ in range(9):
		state.append(int(input()))
	solution = dfid(state)
	if solution:
		print("Solution found in", len(solution), "moves:")
		print(" ".join(solution))
	else:
		print("No solution found within depth limit.")

if __name__ == "__main__":
	main()
