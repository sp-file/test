import os
import tkinter as tk
from tkinter import messagebox

class OSTreeExplorer:
    def __init__(self, root):
        self.root = root
        self.root.title("OS Root Mapper - Interactive Tree")
        self.root.geometry("1000x800")

        # Layout
        self.canvas = tk.Canvas(self.root, bg="white", scrollregion=(0, 0, 5000, 5000))
        self.hbar = tk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.vbar = tk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.canvas.yview)
        
        self.hbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.vbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # State management
        self.nodes = {} # Map canvas IDs to node data
        self.expanded_paths = set()
        
        # Start at root
        self.draw_tree("/", 50, 50)

    def get_color(self, path):
        if not os.access(path, os.R_OK):
            return "#ff6666"  # Red: Access Denied
        if not os.path.isdir(path):
            return "#66b3ff"  # Blue: Application/File
        return "#e1e1e1"      # Grey: Folders

    def draw_tree(self, start_path, start_x, start_y):
        self.canvas.delete("all")
        self.nodes = {}
        self.render_node(start_path, start_x, start_y)

    def render_node(self, path, x, y, level=0):
        name = os.path.basename(path) or "/"
        color = self.get_color(path)
        
        # Draw Box
        box_w, box_h = 140, 30
        rect_id = self.canvas.create_rectangle(x, y, x + box_w, y + box_h, fill=color, outline="black")
        text_id = self.canvas.create_text(x + 5, y + 15, text=name, anchor="w", font=("Arial", 10))
        
        # Store metadata
        self.nodes[rect_id] = {"path": path, "x": x, "y": y, "is_dir": os.path.isdir(path)}
        self.canvas.tag_bind(rect_id, "<Button-1>", lambda e, p=path: self.on_click(p))
        self.canvas.tag_bind(text_id, "<Button-1>", lambda e, p=path: self.on_click(p))

        if path in self.expanded_paths and os.path.isdir(path):
            try:
                children = sorted(os.listdir(path))
                child_y = y + 50
                child_x = x + 40 # Indent children
                
                for child in children:
                    full_path = os.path.join(path, child)
                    # Draw connector line
                    self.canvas.create_line(x + 20, y + 30, x + 20, child_y + 15, x + 40, child_y + 15)
                    
                    # Recursively render (simplified for basic GUI)
                    next_y = self.render_node(full_path, child_x, child_y)
                    child_y = next_y
                return child_y
            except PermissionError:
                pass
        
        return y + 40

    def on_click(self, path):
        if os.path.isdir(path):
            if path in self.expanded_paths:
                self.expanded_paths.remove(path)
            else:
                self.expanded_paths.add(path)
            self.draw_tree("/", 50, 50) # Refresh
        else:
            self.read_file(path)

    def read_file(self, path):
        # Preview window
        win = tk.Toplevel(self.root)
        win.title(f"Preview: {path}")
        text_area = tk.Text(win, wrap=tk.WORD)
        text_area.pack(expand=True, fill="both")

        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(5000) # Read first 5000 chars
                text_area.insert("1.0", content)
        except Exception:
            # Change box color logic would require a refresh, 
            # for now we show an error in the text box
            text_area.insert("1.0", "[LOCKED OR UNREADABLE]")
            text_area.config(bg="#d1b3ff") # Purple tint for unreadable

if __name__ == "__main__":
    root = tk.Tk()
    app = OSTreeExplorer(root)
    root.mainloop()
