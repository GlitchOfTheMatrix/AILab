#include <iostream>
#include <vector>
#include <queue>
#include <set>
#include <algorithm>
#include <map>
using namespace std;

struct State
{
    vector<vector<int>> board;
    int x, y; // position of blank (0)
    vector<string> path;
    State(const vector<vector<int>> &b, int xx, int yy, const vector<string> &p) : board(b), x(xx), y(yy), path(p) {}
    bool operator<(const State &other) const
    {
        return board < other.board;
    }
};

vector<vector<int>> goal = {
    {1, 2, 3},
    {4, 5, 6},
    {7, 8, 0}};

bool isGoal(const vector<vector<int>> &board)
{
    return board == goal;
}

vector<pair<int, int>> directions = {
    {-1, 0}, {1, 0}, {0, -1}, {0, 1}};
vector<string> dirNames = {"Up", "Down", "Left", "Right"};

bool DLS(State state, int depth, set<vector<vector<int>>> &visited, vector<string> &result)
{
    if (isGoal(state.board))
    {
        result = state.path;
        return true;
    }
    if (depth == 0)
        return false;
    visited.insert(state.board);
    for (int d = 0; d < 4; ++d)
    {
        int nx = state.x + directions[d].first;
        int ny = state.y + directions[d].second;
        if (nx >= 0 && nx < 3 && ny >= 0 && ny < 3)
        {
            vector<vector<int>> newBoard = state.board;
            swap(newBoard[state.x][state.y], newBoard[nx][ny]);
            if (visited.count(newBoard))
                continue;
            vector<string> newPath = state.path;
            newPath.push_back(dirNames[d]);
            State next(newBoard, nx, ny, newPath);
            if (DLS(next, depth - 1, visited, result))
                return true;
        }
    }
    visited.erase(state.board);
    return false;
}

bool DFID(State start, int maxDepth, vector<string> &result)
{
    for (int depth = 0; depth <= maxDepth; ++depth)
    {
        set<vector<vector<int>>> visited;
        if (DLS(start, depth, visited, result))
            return true;
    }
    return false;
}

int main()
{
    vector<vector<int>> initial(3, vector<int>(3));
    cout << "Enter the initial 8-puzzle state (use 0 for blank):\n";
    for (int i = 0; i < 3; ++i)
        for (int j = 0; j < 3; ++j)
            cin >> initial[i][j];
    int x = 0, y = 0;
    for (int i = 0; i < 3; ++i)
        for (int j = 0; j < 3; ++j)
            if (initial[i][j] == 0)
            {
                x = i;
                y = j;
            }
    State start(initial, x, y, {});
    vector<string> result;
    int maxDepth = 30; // You can adjust this limit
    if (DFID(start, maxDepth, result))
    {
        cout << "Solution found in " << result.size() << " moves:\n";
        for (const auto &move : result)
            cout << move << " ";
        cout << endl;
    }
    else
    {
        cout << "No solution found within depth limit." << endl;
    }
    return 0;
}
