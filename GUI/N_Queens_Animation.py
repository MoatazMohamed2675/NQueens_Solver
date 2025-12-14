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

        self.is_paused = False
        self.current_step = 0
        self.current_solution = None
        self.current_n = 0

        main = ttk.Frame(root, padding=10)
        main.pack(fill="both", expand=True)

        # ---------------- LEFT CONTROL PANEL ----------------
        control = ttk.Frame(main)
        control.pack(side="left", fill="y", padx=10)

        ttk.Label(control, text="Board Size (N):").pack()
        self.n_entry = ttk.Entry(control, width=10)
        self.n_entry.insert(0, "8")
        self.n_entry.pack(pady=5)

        ttk.Label(control, text="Algorithm:").pack()
        self.alg_choice = ttk.Combobox(
            control,
            values=[
                "Hill Climbing",
                "Cultural Algorithm",
                "Back Tracking",
                "Best First Search"
            ],
            state="readonly"
        )
        self.alg_choice.current(0)
        self.alg_choice.pack(pady=5)
        self.alg_choice.bind("<<ComboboxSelected>>", self.toggle_ca_fields)

        # -------- Cultural Algorithm Extra Inputs --------
        self.ca_frame = ttk.LabelFrame(control, text="CA Parameters")

        ttk.Label(self.ca_frame, text="Population Size:").pack(anchor="w")
        self.pop_entry = ttk.Entry(self.ca_frame, width=10)
        self.pop_entry.insert(0, "350")
        self.pop_entry.pack(pady=2)

        ttk.Label(self.ca_frame, text="Mutation Rate:").pack(anchor="w")
        self.mut_entry = ttk.Entry(self.ca_frame, width=10)
        self.mut_entry.insert(0, "0.2")
        self.mut_entry.pack(pady=2)

        ttk.Label(self.ca_frame, text="Max Generations:").pack(anchor="w")
        self.gen_entry = ttk.Entry(self.ca_frame, width=10)
        self.gen_entry.insert(0, "5000")
        self.gen_entry.pack(pady=2)

        self.ca_frame.pack_forget()

        ttk.Button(control, text="Solve", command=self.solve).pack(pady=5)
        ttk.Button(control, text="Pause", command=self.pause).pack(pady=5)
        ttk.Button(control, text="Resume", command=self.resume).pack(pady=5)

        # ---------------- RIGHT SIDE ----------------
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
        if self.alg_choice.get() == "Cultural Algorithm":
            self.ca_frame.pack(pady=10, fill="x")
        else:
            self.ca_frame.pack_forget()

    # --------------------------------------------------------
    def log(self, text):
        self.log_box.insert(tk.END, text + "\n")
        self.log_box.see(tk.END)

    # --------------------------------------------------------
    def pause(self):
        self.is_paused = True
        self.log("⏸ Animation paused")

    def resume(self):
        if self.current_solution is not None:
            self.is_paused = False
            self.log("▶ Animation resumed")
            self.animate_solution()

    # --------------------------------------------------------
    def animate_solution(self):
        if self.is_paused:
            return

        solution = self.current_solution
        n = self.current_n
        step = self.current_step

        self.canvas.delete("all")
        cell = self.canvas_size / n

        # Draw board
        for r in range(n):
            for c in range(n):
                x1, y1 = c * cell, r * cell
                x2, y2 = x1 + cell, y1 + cell
                color = "#F0D9B5" if (r + c) % 2 == 0 else "#B58863"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

        # Draw queens
        for r in range(step + 1):
            c = solution[r]
            cx = c * cell + cell / 2
            cy = r * cell + cell / 2
            self.canvas.create_text(cx, cy, text="♛", font=("Arial", int(cell * 0.7)))

        self.log(f"Step {step + 1}: Queen at row {step}, column {solution[step]}")

        self.current_step += 1

        if self.current_step < n:
            self.root.after(500, self.animate_solution)

    # --------------------------------------------------------
    def solve(self):
        self.log_box.delete("1.0", tk.END)
        self.is_paused = False
        self.current_step = 0

        try:
            n = int(self.n_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "N must be an integer")
            return

        if n < 4:
            messagebox.showerror("Invalid Board Size", "N must be 4 or greater.")
            return

        algo = self.alg_choice.get()
        self.log(f"Running {algo}...")

        start = time.time()

        if algo == "Hill Climbing":
            solution = HillClimbing(n).solve()

        elif algo == "Cultural Algorithm":
            solver = CulturalAlgorithm(
                n,
                int(self.pop_entry.get()),
                float(self.mut_entry.get()),
                int(self.gen_entry.get())
            )
            solution = solver.run(log_callback=self.log)

        elif algo == "Back Tracking":
            solver = BackTracking()
            solutions = solver.solveNQueens(n)
            if not solutions:
                self.log("No solution found.")
                return
            solution = [row.index("Q") for row in solutions[0]]

        else:
            solver = SolutionBestFS()
            solutions = solver.solveNQueens(n)
            if not solutions:
                self.log("No solution found.")
                return
            solution = [row.index("Q") for row in solutions[0]]

        if solution is None:
            self.log("No solution found.")
            return

        elapsed = time.time() - start
        self.log(f"Solution found in {elapsed:.4f} seconds")

        self.current_solution = solution
        self.current_n = n
        self.animate_solution()


# --------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = NQueensGUI(root)
    root.mainloop()
