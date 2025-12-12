import heapq

class SolutionBestFS:
    def heuristic(self, queens):
        return -len(queens)

    def solveNQueens(self, n: int):
        res = []
        pq = []
        
        start_state = (0, 0, [], set(), set(), set())
        heapq.heappush(pq, start_state)
        
        while pq:
            priority, row, queens, cols, posDiag, negDiag = heapq.heappop(pq)
            
            if row == n:
                board = []
                for c in queens:
                    row_str = '.' * c + 'Q' + '.' * (n - c - 1)
                    board.append(row_str)
                res.append(board)
                continue
            
            for c in range(n):
                if c in cols or (row + c) in posDiag or (row - c) in negDiag:
                    continue
                
                new_queens = queens + [c]
                h = self.heuristic(new_queens)
                
                heapq.heappush(pq, (
                    h,
                    row + 1,
                    new_queens,
                    cols | {c},
                    posDiag | {row + c},
                    negDiag | {row - c}
                ))
        
        return res

