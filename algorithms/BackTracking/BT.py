class BackTracking:
    def solveNQueens(self, n: int) -> list[list[str]]:
        col = set()
        pstDiag = set()
        negDiag = set()

        res = []
        board = [["."] * n for _ in range(n)]

        def backtracking(r):
            if r == n:
                copy = ["".join(row) for row in board]
                res.append(copy)
                return

            for c in range(n):
                if c in col or (r + c) in pstDiag or (r - c) in negDiag:
                    continue

                col.add(c)
                pstDiag.add(r + c)
                negDiag.add(r - c)
                board[r][c] = 'Q'

                backtracking(r + 1)

                col.remove(c)
                pstDiag.remove(r + c)
                negDiag.remove(r - c)
                board[r][c] = '.'

        backtracking(0)
        return res
