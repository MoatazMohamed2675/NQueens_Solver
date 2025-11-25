import tkinter as tk
from tkinter import ttk, messagebox
import time

# --- IMAGE HANDLING ---
HAS_PIL = False
try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    pass

class NQueensApp:
    def __init__(self, root):
        self.root = root
        self.root.title("N-Queens Solver (Final)")
        self.root.geometry("1100x800")
        self.root.configure(bg="#2c3e50")

        # --- Variables ---
        self.n_var = tk.IntVar(value=8)
        self.algo_var = tk.StringVar(value="Backtracking")
        self.speed_var = tk.DoubleVar(value=0.05)
        self.anim_var = tk.BooleanVar(value=True)  # New: Toggle Animation
        
        self.status_var = tk.StringVar(value="Ready")
        self.result_var = tk.StringVar(value="Time: 0.00s | Steps: 0") # New: Results
        
        self.is_running = False
        self.generator = None
        self.start_time = 0
        
        # Image Cache
        self.cached_image = None
        self.last_cell_size = 0
        self.load_queen_image()

        # --- Layout ---
        self.setup_ui()
        self.root.after(100, lambda: self.draw_board([]))

    def load_queen_image(self):
        self.pil_image = None
        self.tk_image_raw = None
        self.using_custom_image = False
        try:
            if HAS_PIL:
                self.pil_image = Image.open("queen.png")
                self.using_custom_image = True
            else:
                self.tk_image_raw = tk.PhotoImage(file="queen.png")
                self.using_custom_image = True
        except:
            print("Image not found, using Vector Crown.")
            self.using_custom_image = False

    def setup_ui(self):
        # SIDEBAR
        sidebar = tk.Frame(self.root, bg="#34495e", width=280, padx=20, pady=20)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        # Header
        tk.Label(sidebar, text="N-Queens", font=("Segoe UI", 22, "bold"), bg="#34495e", fg="white").pack(pady=(0, 20))

        # Inputs
        tk.Label(sidebar, text="Board Size (N)", bg="#34495e", fg="#ecf0f1").pack(anchor="w")
        tk.Entry(sidebar, textvariable=self.n_var, font=("Segoe UI", 12)).pack(fill=tk.X, pady=(5, 15))

        tk.Label(sidebar, text="Algorithm", bg="#34495e", fg="#ecf0f1").pack(anchor="w")
        options = ["Backtracking", "Best-First Search", "Hill-Climbing", "Cultural Algorithm"]
        self.algo_menu = ttk.Combobox(sidebar, textvariable=self.algo_var, values=options, state="readonly", font=("Segoe UI", 11))
        self.algo_menu.current(0)
        self.algo_menu.pack(fill=tk.X, pady=(5, 15))

        # Animation Controls
        ttk.Checkbutton(sidebar, text="Show Animation", variable=self.anim_var, style="TCheckbutton").pack(anchor="w", pady=(5, 5))
        
        tk.Label(sidebar, text="Speed (if animating)", bg="#34495e", fg="#bdc3c7", font=("Segoe UI", 9)).pack(anchor="w")
        tk.Scale(sidebar, from_=0.0, to=0.3, resolution=0.01, orient=tk.HORIZONTAL, variable=self.speed_var, bg="#34495e", fg="white", highlightthickness=0).pack(fill=tk.X, pady=(0, 20))

        # Actions
        self.btn_run = tk.Button(sidebar, text="SOLVE", bg="#27ae60", fg="white", font=("Segoe UI", 11, "bold"), relief="flat", command=self.start_solving)
        self.btn_run.pack(fill=tk.X, pady=5)

        self.btn_stop = tk.Button(sidebar, text="STOP", bg="#c0392b", fg="white", font=("Segoe UI", 11, "bold"), relief="flat", command=self.stop_solving)
        self.btn_stop.pack(fill=tk.X, pady=5)

        # Stats Area
        tk.Label(sidebar, textvariable=self.status_var, bg="#34495e", fg="#bdc3c7", font=("Segoe UI", 10, "italic"), wraplength=240).pack(side=tk.BOTTOM, pady=(5, 20))
        tk.Label(sidebar, textvariable=self.result_var, bg="#34495e", fg="#f1c40f", font=("Segoe UI", 11, "bold"), wraplength=240).pack(side=tk.BOTTOM, pady=(20, 5))

        # MAIN CANVAS
        self.canvas_area = tk.Frame(self.root, bg="#2c3e50")
        self.canvas_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.canvas = tk.Canvas(self.canvas_area, bg="#ecf0f1", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Style customization for Checkbox
        style = ttk.Style()
        style.configure("TCheckbutton", background="#34495e", foreground="white", font=("Segoe UI", 11))

    def draw_board(self, board_state):
        self.canvas.delete("all")
        try:
            n = self.n_var.get()
        except: return
        if n < 4: return

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        padding = 20
        size = min(w, h) - (padding * 2)
        cell_size = size / n
        x_start = (w - size) / 2
        y_start = (h - size) / 2

        # PREPARE IMAGE (Resize only if cell size changed)
        if self.using_custom_image and cell_size > 0:
            target_size = int(cell_size * 0.8) # 80% of cell
            if target_size != self.last_cell_size:
                self.update_cached_image(target_size)
                self.last_cell_size = target_size

        for row in range(n):
            for col in range(n):
                x1 = x_start + col * cell_size
                y1 = y_start + row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                color = "#ecf0f1" if (row + col) % 2 == 0 else "#95a5a6"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

                if row < len(board_state) and board_state[row] == col:
                    cx = x1 + cell_size / 2
                    cy = y1 + cell_size / 2
                    self.draw_queen(cx, cy, cell_size)


    def update_cached_image(self, size):
        if HAS_PIL and self.pil_image:
            resized = self.pil_image.resize((size, size), Image.Resampling.LANCZOS)
            self.cached_image = ImageTk.PhotoImage(resized)
        elif self.tk_image_raw:
            orig_w = self.tk_image_raw.width()
            scale = int(orig_w / size)
            if scale < 1: scale = 1
            self.cached_image = self.tk_image_raw.subsample(scale)

    def draw_queen(self, cx, cy, cell_size):
        if self.using_custom_image and self.cached_image:
            self.canvas.create_image(cx, cy, image=self.cached_image, anchor="center")
        else:
            self.draw_vector_crown(cx - cell_size/2, cy - cell_size/2, cell_size)

    # def draw_vector_crown(self, x, y, size):
    #     pad = size * 0.15
    #     wx, wy = x + pad, y + pad
    #     w, h = size - 2 * pad, size - 2 * pad
    #     base_coords = [wx + w*0.2, wy + h*0.9, wx + w*0.8, wy + h*0.9, wx + w*0.85, wy + h*0.6, wx + w*0.15, wy + h*0.6]
    #     spikes_coords = [wx + w*0.15, wy + h*0.6, wx + w*0.05, wy + h*0.2, wx + w*0.35, wy + h*0.5, wx + w*0.5, wy + h*0.1, wx + w*0.65, wy + h*0.5, wx + w*0.95, wy + h*0.2, wx + w*0.85, wy + h*0.6]
    #     self.canvas.create_oval(x + size*0.1, y + size*0.8, x + size*0.9, y + size*0.95, fill="#000000", stipple="gray50", outline="")
    #     self.canvas.create_polygon(base_coords, fill="#f1c40f", outline="#e67e22", width=2)
    #     self.canvas.create_polygon(spikes_coords, fill="#f1c40f", outline="#e67e22", width=2)
    #     self.canvas.create_oval(wx + w*0.5 - w*0.06, wy + h*0.75 - w*0.06, wx + w*0.5 + w*0.06, wy + h*0.75 + w*0.06, fill="#e74c3c", outline="white")

    # --- SOLVER CONTROL ---
    def start_solving(self):
        if self.is_running: return
        try:
            n = self.n_var.get()
            if n < 4: raise ValueError
        except:
            messagebox.showerror("Error", "Please enter N >= 4")
            return

        self.is_running = True
        self.btn_run.config(state="disabled")
        self.status_var.set("Initializing...")
        self.result_var.set("Calculating...")
        
        # Select Algorithm
        algo = self.algo_var.get()
        if algo == "Backtracking": self.generator = self.run_backtracking(n)
        elif algo == "Best-First Search": self.generator = self.run_placeholder(n, "Best-First")
        elif algo == "Hill-Climbing": self.generator = self.run_placeholder(n, "Hill-Climbing")
        elif algo == "Cultural Algorithm": self.generator = self.run_placeholder(n, "Cultural Algo")

        self.start_time = time.time()

        if self.anim_var.get():
            # Run with animation
            self.animate_step()
        else:
            # Run instantly
            self.solve_instantly()

    def stop_solving(self):
        self.is_running = False
        self.generator = None
        self.btn_run.config(state="normal")
        self.status_var.set("Stopped by user")
        self.draw_board([])

    def solve_instantly(self):
        """Loops through the generator as fast as possible without drawing."""
        final_board = []
        final_steps = 0
        success = False
        
        try:
            # We consume the generator
            for status, data, steps in self.generator:
                if status == 'done':
                    final_board = data
                    final_steps = steps
                    success = True
                    break
                elif status == 'fail':
                    final_steps = steps
                    success = False
                    break
            
            elapsed = time.time() - self.start_time
            self.finish_run(success, final_board, final_steps, elapsed)
            
        except Exception as e:
            print(f"Error: {e}")
            self.stop_solving()

    def animate_step(self):
        """Runs one step, draws it, and schedules the next."""
        if not self.is_running: return

        try:
            # Fetch next step
            status, data, steps = next(self.generator)
            
            if status == 'step':
                self.draw_board(data)
                self.status_var.set(f"Working... Steps: {steps}")
                
                # Schedule next
                delay = int(self.speed_var.get() * 1000)
                self.root.after(max(1, delay), self.animate_step)
            
            elif status == 'done':
                elapsed = time.time() - self.start_time
                self.finish_run(True, data, steps, elapsed)

            elif status == 'fail':
                elapsed = time.time() - self.start_time
                self.finish_run(False, [], steps, elapsed)

        except StopIteration:
            self.stop_solving()

    def finish_run(self, success, board, steps, time_taken):
        self.is_running = False
        self.btn_run.config(state="normal")
        
        if success:
            self.draw_board(board)
            self.status_var.set("Solution Found!")
            self.result_var.set(f"Time: {time_taken:.4f}s | Steps: {steps}")
            # Optional: Show popup only if it took a long time, otherwise just text
            if time_taken > 1.0:
                messagebox.showinfo("Success", f"Solved in {time_taken:.4f}s\nTotal Steps: {steps}")
        else:
            self.status_var.set("No Solution Found")
            self.result_var.set(f"Time: {time_taken:.4f}s | Steps: {steps}")
            messagebox.showinfo("Result", "No solution found.")

    # =========================================================================
    # ALGORITHMS
    # =========================================================================
    
    # 1. Backtracking
    def run_backtracking(self, n):
        board = [-1] * n
        stack = [(0, 0)] 
        steps = 0

        while stack:
            row, col = stack.pop()
            
            if row < 0:
                yield ('fail', None, steps)
                return

            if row == n:
                yield ('done', board, steps)
                return

            placed = False
            for c in range(col, n):
                steps += 1
                
                # Check safety
                safe = True
                for r_prev in range(row):
                    c_prev = board[r_prev]
                    if c_prev == c or abs(c_prev - c) == abs(r_prev - row):
                        safe = False
                        break
                
                if safe:
                    board[row] = c
                    # Yield step data: (status, current_board, current_step_count)
                    yield ('step', board[:row+1], steps)
                    
                    stack.append((row, c + 1))
                    stack.append((row + 1, 0))
                    placed = True
                    break
            
            if not placed:
                board[row] = -1
                pass

    # Placeholders
    def run_placeholder(self, n, name):
        yield ('step', [], 0)
        time.sleep(0.5)
        yield ('fail', [], 0)
        messagebox.showinfo("Info", f"{name} is not implemented yet.\nConnect your code in the bottom section.")

if __name__ == "__main__":
    root = tk.Tk()
    app = NQueensApp(root)
    root.mainloop()