#include <bits/stdc++.h>
using namespace std;

// Manhattan Distance Heuristic
int manhattan(string state, string goal)
{
    int dist = 0;
    for (int i = 0; i < 9; i++)
    {
        if (state[i] != '_')
        {
            int gi = goal.find(state[i]);
            dist += abs(i / 3 - gi / 3) + abs(i % 3 - gi % 3);
        }
    }
    return dist;
}

// Node for Priority Queue
struct Node
{
    string state;
    int g, f;
    vector<string> path;
    bool operator>(const Node &other) const
    {
        return f > other.f;
    }
};

// A* Search
vector<string> solve(string start, string goal)
{
    priority_queue<Node, vector<Node>, greater<Node>> pq;
    set<string> visited;

    pq.push({start, 0, manhattan(start, goal), {start}});

    while (!pq.empty())
    {
        Node cur = pq.top();
        pq.pop();

        if (cur.state == goal)
            return cur.path;
        if (visited.count(cur.state))
            continue;
        visited.insert(cur.state);

        int i = cur.state.find('_');
        vector<int> moves;

        if (i > 2)
            moves.push_back(i - 3); // up
        if (i < 6)
            moves.push_back(i + 3); // down
        if (i % 3 != 0)
            moves.push_back(i - 1); // left
        if (i % 3 != 2)
            moves.push_back(i + 1); // right

        for (int m : moves)
        {
            string new_state = cur.state;
            swap(new_state[i], new_state[m]);
            if (!visited.count(new_state))
            {
                int g = cur.g + 1;
                int h = manhattan(new_state, goal);
                vector<string> new_path = cur.path;
                new_path.push_back(new_state);
                pq.push({new_state, g, g + h, new_path});
            }
        }
    }
    return {};
}

int main()
{
    string start = "2831647_5"; // Example start
    string goal = "1238_4765";  // Example goal

    cout << "Start: " << start << "\nGoal : " << goal << "\n\n";

    vector<string> path = solve(start, goal);

    if (!path.empty())
    {
        cout << "Solution found in " << path.size() - 1 << " moves:\n";
        for (string step : path)
        {
            for (int i = 0; i < 9; i++)
            {
                cout << step[i] << " ";
                if (i % 3 == 2)
                    cout << "\n";
            }
            cout << "\n";
        }
    }
    else
    {
        cout << "No solution found.\n";
    }
}