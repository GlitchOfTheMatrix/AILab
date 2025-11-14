# AO* on a small AND-OR graph (acyclic)
# Representation:
#   node -> {
#       "type": "OR" | "AND",
#       "cost": h_or_base_cost,          # used for leaves; 0 for internal nodes
#       "edges": [ (child, edge_cost), ... ]
#   }
# AND is encoded by a single edge to a TUPLE of child node names: (("C","D"), edge_cost)

from math import inf
from functools import lru_cache

def is_leaf(G, n):
    return len(G[n]["edges"]) == 0

def expand_and_tuple(tnode):
    # tnode is a tuple of node names, e.g., ("C", "D")
    return list(tnode)

class AOStar:
    def __init__(self, graph, start):
        self.G = graph
        self.start = start
        # Best cost estimate (final exact cost after solve)
        self.H = {n: graph[n]["cost"] for n in graph}
        # Best policy: for OR nodes -> best child; for AND nodes -> the AND-tuple
        self.best_child = {n: None for n in graph}

    @lru_cache(maxsize=None)
    def solve(self, node):
        """
        Returns the minimal cost from 'node' to a terminal solution graph.
        Populates self.H[node] and self.best_child[node].
        """
        # Leaf: its cost is already given (heuristic/base cost)
        if is_leaf(self.G, node):
            self.best_child[node] = None
            self.H[node] = self.G[node]["cost"]
            return self.H[node]

        typ = self.G[node]["type"]
        edges = self.G[node]["edges"]

        if typ == "OR":
            best_cost = inf
            best = None
            for (child, ec) in edges:
                # Recurse to get the child's minimal solution cost
                child_cost = self.solve(child)
                total = ec + child_cost
                if total < best_cost:
                    best_cost = total
                    best = child
            self.best_child[node] = best
            self.H[node] = best_cost
            return best_cost

        else:  # AND node (single edge to a tuple of children)
            assert len(edges) == 1, "Each AND node should have exactly one AND edge."
            (tnode, ec) = edges[0]
            children = expand_and_tuple(tnode)
            total_children = 0
            for ch in children:
                total_children += self.solve(ch)
            total = ec + total_children
            self.best_child[node] = tnode
            self.H[node] = total
            return total

    def extract_solution(self):
        """
        Walks the chosen policy to list the solution graph nodes.
        """
        sol = []
        seen = set()

        def dfs(n):
            if n in seen:
                return
            seen.add(n)
            sol.append(n)
            bc = self.best_child[n]
            if bc is None:
                return
            if isinstance(bc, tuple):  # AND: expand all
                for ch in bc:
                    dfs(ch)
            else:  # OR: follow best child
                dfs(bc)

        dfs(self.start)
        return sol

if __name__ == "__main__":
    # Example graph (acyclic):
    # S (OR) -> A (edge 1), B (edge 2)
    # A (AND) -> (C, D) with edge cost 2
    # B (OR)  -> E (edge 1), F (edge 3)
    # Leaves C,D,E,F with base costs as shown
    G = {
        "S": {"type": "OR",  "cost": 0, "edges": [("A", 1), ("B", 2)]},
        "A": {"type": "AND", "cost": 0, "edges": [(("C", "D"), 2)]},
        "B": {"type": "OR",  "cost": 0, "edges": [("E", 1), ("F", 3)]},
        "C": {"type": "OR",  "cost": 2, "edges": []},  # leaf
        "D": {"type": "OR",  "cost": 1, "edges": []},  # leaf
        "E": {"type": "OR",  "cost": 1, "edges": []},  # leaf
        "F": {"type": "OR",  "cost": 4, "edges": []},  # leaf
    }

    ao = AOStar(G, "S")
    total_cost = ao.solve("S")
    print("Total minimal cost from S:", total_cost)
    print("Best costs (H):", ao.H)
    print("Policy (best_child):", ao.best_child)
    print("Solution graph walk:", " -> ".join(ao.extract_solution()))
