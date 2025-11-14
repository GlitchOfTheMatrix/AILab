#include <iostream>
#include <vector>
#include <queue>
#include <map>
#include <cmath>
#include <algorithm>

using namespace std;

// Structure to represent a state in the 8-puzzle
struct State
{
    vector<vector<int>> board;
    int g;       // Cost from start to current state
    int h;       // Heuristic cost from current state to goal
    int f;       // g + h
    string path; // Path taken to reach this state

    // Custom comparator for priority queue (min-heap based on f-value)
    bool operator>(const State &other) const
    {
        return f > other.f;
    }
};

// Function to calculate Manhattan distance heuristic
int calculateManhattanDistance(const vector<vector<int>> &board)
{
    int manhattanDistance = 0;
    for (int i = 0; i < 3; ++i)
    {
        for (int j = 0; j < 3; ++j)
        {
            int value = board[i][j];
            if (value != 0)
            { // 0 is the empty tile
                int targetRow = (value - 1) / 3;
                int targetCol = (value - 1) % 3;
                manhattanDistance += abs(i - targetRow) + abs(j - targetCol);
            }
        }
    }
    return manhattanDistance;
}

// Function to find the position of the empty tile (0)
pair<int, int> findEmptyTile(const vector<vector<int>> &board)
{
    for (int i = 0; i < 3; ++i)
    {
        for (int j = 0; j < 3; ++j)
        {
            if (board[i][j] == 0)
            {
                return {i, j};
            }
        }
    }
    return {-1, -1}; // Should not happen in a valid 8-puzzle
}

// Function to get possible next states
vector<State> getNextStates(const State &currentState)
{
    vector<State> nextStates;
    pair<int, int> emptyPos = findEmptyTile(currentState.board);
    int row = emptyPos.first;
    int col = emptyPos.second;

    // Possible moves for the empty tile: Up, Down, Left, Right
    int dr[] = {-1, 1, 0, 0};
    int dc[] = {0, 0, -1, 1};
    char move_char[] = {'U', 'D', 'L', 'R'};

    for (int i = 0; i < 4; ++i)
    {
        int newRow = row + dr[i];
        int newCol = col + dc[i];

        // Check if the new position is within the board
        if (newRow >= 0 && newRow < 3 && newCol >= 0 && newCol < 3)
        {
            vector<vector<int>> newBoard = currentState.board;
            swap(newBoard[row][col], newBoard[newRow][newCol]);

            State nextState;
            nextState.board = newBoard;
            nextState.g = currentState.g + 1;
            nextState.h = calculateManhattanDistance(newBoard);
            nextState.f = nextState.g + nextState.h;
            nextState.path = currentState.path + move_char[i];
            nextStates.push_back(nextState);
        }
    }
    return nextStates;
}

// Function to solve the 8-puzzle using A* search
void solve8Puzzle(const vector<vector<int>> &initialBoard)
{
    priority_queue<State, vector<State>, greater<State>> openList;
    map<vector<vector<int>>, int> costMap; // To track the minimum cost to reach a state

    State startState;
    startState.board = initialBoard;
    startState.g = 0;
    startState.h = calculateManhattanDistance(initialBoard);
    startState.f = startState.g + startState.h;
    startState.path = "";

    openList.push(startState);
    costMap[initialBoard] = 0;

    vector<vector<int>> goalBoard = {{1, 2, 3}, {4, 5, 6}, {7, 8, 0}};

    while (!openList.empty())
    {
        State currentState = openList.top();
        openList.pop();

        if (currentState.board == goalBoard)
        {
            cout << "Goal state reached!" << endl;
            cout << "Path: " << currentState.path << endl;
            cout << "Number of moves: " << currentState.g << endl;
            return;
        }

        vector<State> nextStates = getNextStates(currentState);
        for (const auto &nextState : nextStates)
        {
            // If we haven't seen this state before, or we found a cheaper path to it
            if (costMap.find(nextState.board) == costMap.end() || nextState.g < costMap[nextState.board])
            {
                costMap[nextState.board] = nextState.g;
                openList.push(nextState);
            }
        }
    }

    cout << "No solution found." << endl;
}

// Main function to run the solver
int main()
{
    vector<vector<int>> initialBoard = {
        {1, 2, 3},
        {0, 4, 6},
        {7, 5, 8}};

    cout << "Solving 8-puzzle..." << endl;
    cout << "Initial state:" << endl;
    for (const auto &row : initialBoard)
    {
        for (int val : row)
        {
            cout << val << " ";
        }
        cout << endl;
    }
    cout << endl;

    solve8Puzzle(initialBoard);

    return 0;
}
