import random

class HillClimbing:
    def __init__(self, n, max_restarts=200):
        self.n = n
        self.max_restarts = max_restarts

    # -----------------------------
    # Count Conflicts
    # -----------------------------
    def count_conflicts(self, board):
        conflicts = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if board[i] == board[j]:
                    conflicts += 1
                if abs(board[i] - board[j]) == abs(i - j):
                    conflicts += 1
        return conflicts

    # -----------------------------
    # Generate Random Board
    # -----------------------------
    def generate_random_board(self):
        return [random.randint(0, self.n - 1) for _ in range(self.n)]

    # -----------------------------
    # Hill Climbing Algorithm
    # -----------------------------
    def solve(self):
        for restart in range(self.max_restarts):
            board = self.generate_random_board()
            current_conflicts = self.count_conflicts(board)

            while True:
                best_board = board.copy()
                best_conflicts = current_conflicts

                # Try all neighbours
                for row in range(self.n):
                    for col in range(self.n):
                        if board[row] == col:
                            continue
                        new_board = board.copy()
                        new_board[row] = col
                        new_conflicts = self.count_conflicts(new_board)

                        if new_conflicts < best_conflicts:
                            best_board = new_board.copy()
                            best_conflicts = new_conflicts

                # No improvement → stuck
                if best_conflicts >= current_conflicts:
                    break

                # Move to better neighbour
                board = best_board.copy()
                current_conflicts = best_conflicts

            # Found valid solution
            if current_conflicts == 0:
                return board

        return None
