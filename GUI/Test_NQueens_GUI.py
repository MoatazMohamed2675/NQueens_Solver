import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import scrolledtext
import time
import sys, os

# Adjust path for your modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from algorithms.Hill_Climbing.Hill_Climbing_Algorithm import HillClimbing
from algorithms.Cultural_Algorithm.CA import CulturalAlgorithm
from algorithms.BackTracking.BT import BackTracking
from algorithms.Best_First_Search.BFS import SolutionBestFS

class NQueensGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("N-Queens Solver GUI")

        main = ttk.Frame(root, padding=10)
        main.pack(fill="both", expand=True)

        # ---------------- LEFT CONTROL PANEL ----------------
        control = ttk.Frame(main)
        control.pack(side="left", fill="y", padx=10)

        # N input
        ttk.Label(control, text="Board Size (N):").pack()
        self.n_entry = ttk.Entry(control, width=10)
        self.n_entry.insert(0, "8")
        self.n_entry.pack(pady=5)

        # Algorithm selection
        ttk.Label(control, text="Algorithm:").pack()
        self.alg_choice = ttk.Combobox(control, values=["Hill Climbing", "Cultural Algorithm", "Back Tracking", "Best First Search"], state="readonly")
        self.alg_choice.current(0)
        self.alg_choice.pack(pady=5)
        self.alg_choice.bind("<<ComboboxSelected>>", self.toggle_ca_fields)

        # -------- Cultural Algorithm Extra Inputs --------
        self.ca_frame = ttk.LabelFrame(control, text="CA Parameters")
        
        ttk.Label(self.ca_frame, text="Population Size:").pack(anchor="w")
        self.pop_entry = ttk.Entry(self.ca_frame, width=10)
        self.pop_entry.insert(0, "300")
        self.pop_entry.pack(pady=2)

        ttk.Label(self.ca_frame, text="Mutation Rate:").pack(anchor="w")
        self.mut_entry = ttk.Entry(self.ca_frame, width=10)
        self.mut_entry.insert(0, "0.01")
        self.mut_entry.pack(pady=2)

        ttk.Label(self.ca_frame, text="Max Generations:").pack(anchor="w")
        self.gen_entry = ttk.Entry(self.ca_frame, width=10)
        self.gen_entry.insert(0, "5000")
        self.gen_entry.pack(pady=2)

        # Hide CA fields initially
        self.ca_frame.pack_forget()

        # Solve button
        ttk.Button(control, text="Solve", command=self.solve).pack(pady=10)

        # ---------------- RIGHT CANVAS + LOG ----------------
        right = ttk.Frame(main)
        right.pack(side="right", fill="both", expand=True)

        self.canvas_size = 400
        self.canvas = tk.Canvas(right, width=self.canvas_size, height=self.canvas_size, bg="white")
        self.canvas.pack(pady=10)

        ttk.Label(right, text="Log:").pack(anchor="w")
        self.log_box = scrolledtext.ScrolledText(right, height=10, width=50)
        self.log_box.pack(fill="both", expand=True)

    # --------------------------------------------------------
    def toggle_ca_fields(self, event=None):
        """Show CA fields only when CA is selected."""
        if self.alg_choice.get() == "Cultural Algorithm":
            self.ca_frame.pack(pady=10, fill="x")
        else:
            self.ca_frame.pack_forget()

    # --------------------------------------------------------
    def draw_board(self, solution, n):
        """Draw chessboard + queens as Unicode icons."""
        self.canvas.delete("all")
        cell = self.canvas_size / n

        for r in range(n):
            for c in range(n):
                x1, y1 = c * cell, r * cell
                x2, y2 = x1 + cell, y1 + cell
                color = "#F0D9B5" if (r + c) % 2 == 0 else "#B58863"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

        # Draw Unicode queen
        for r, c in enumerate(solution):
            cx = c * cell + cell / 2
            cy = r * cell + cell / 2
            self.canvas.create_text(cx, cy, text="♛", font=("Arial", int(cell * 0.7)))

    # --------------------------------------------------------
    def log(self, text):
        self.log_box.insert(tk.END, text + "\n")
        self.log_box.see(tk.END)

    # --------------------------------------------------------
    def solve(self):
        self.log_box.delete("1.0", tk.END)

        try:
            n = int(self.n_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "N must be an integer")
            return

        algo = self.alg_choice.get()
        self.log(f"Running {algo}...")

        start = time.time()

        # ---------- Hill Climbing ----------
        if algo == "Hill Climbing":
            solver = HillClimbing(n)
            solution = solver.solve()

        # ---------- Cultural Algorithm ----------
        elif algo == "Cultural Algorithm":
            try:
                pop = int(self.pop_entry.get())
                mut = float(self.mut_entry.get())
                gen = int(self.gen_entry.get())
            except ValueError:
                messagebox.showerror("Invalid Input", "CA parameters must be numeric")
                return

            solver = CulturalAlgorithm(
                n,
                population_size=pop,
                mutation_rate=mut,
                max_generations=gen
            )

            # Pass GUI log callback
            solution = solver.run(log_callback=self.log)
                
        # ---------- Backtracking ----------
        elif algo == "Back Tracking":
            solver = BackTracking()
            solution = solver.solveNQueens(n)

            if not solution:
                self.log("No solution found.")
                return

            board = solution[0]

            # Convert each string row to the column index of Q
            solution = []
            for row in board:
                solution.append(row.index("Q"))

        # ---------- Best First Search ----------
        else:
            solver = SolutionBestFS()
            solutions = solver.solveNQueens(n)

            if not solutions:
                self.log("No solution found.")
                return

            # Pick the first solution
            board = solutions[0]

            # Convert each string row to the column index of 'Q'
            solution = []
            for row in board:
                solution.append(row.index("Q"))
                

        elapsed = time.time() - start

        if solution is None:
            self.log("No solution found.")
            return

        self.draw_board(solution, n)
        self.log(f"Solution: {solution}")
        self.log(f"Time: {elapsed:.4f} seconds")


# --------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = NQueensGUI(root)
    root.mainloop()
