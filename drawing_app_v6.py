import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
from tkinter import filedialog
from PIL import Image

# Constants
BACKGROUND_COLOR = "white"
BRUSH = "brush"
ERASER = "eraser"
PENCIL = "pencil"

class DrawingApp:
    def __init__(self):
        self.previous_x = None
        self.previous_y = None

        # Initialize the Tkinter window and set its title
        self.window = tk.Tk()
        self.window.title("Drawing App")

        # Set the window size and make it non-resizable
        self.window.geometry("800x600")
        self.window.resizable(False, False)

        # Global variables
        self.drawing_color = tk.StringVar()
        self.drawing_color.set("black")
        self.drawing_tool = tk.StringVar()
        self.drawing_tool.set("brush")
        self.line_width = tk.IntVar()
        self.line_width.set(5)

        self.undo_stack = []
        self.redo_stack = []

        self.setup_canvas()
        self.setup_toolbar()

    def setup_canvas(self):
        """Set up the canvas for drawing."""
        self.canvas = tk.Canvas(self.window, bg=BACKGROUND_COLOR)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Bind mouse events for drawing
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

    def setup_toolbar(self):
        """Set up the toolbar with buttons."""
        self.toolbar = tk.Frame(self.window, bg="lightgray")
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Add buttons for brush, color picker, eraser, and clear canvas
        brush_button = ttk.Button(self.toolbar, text="Brush", command=self.use_brush)
        color_button = ttk.Button(self.toolbar, text="Color", command=self.choose_color)
        eraser_button = ttk.Button(self.toolbar, text="Eraser", command=self.use_eraser)
        pencil_button = ttk.Button(self.toolbar, text="Pencil", command=self.use_pencil)
        clear_button = ttk.Button(self.toolbar, text="Clear", command=self.clear_canvas)
        save_button = ttk.Button(self.toolbar, text="Save", command=self.save_drawing)
        undo_button = ttk.Button(self.toolbar, text="Undo", command=self.undo)
        redo_button = ttk.Button(self.toolbar, text="Redo", command=self.redo)

        # Add slider for changing line width
        line_width_slider = ttk.Scale(self.toolbar, from_=1, to=30, orient=tk.HORIZONTAL, variable=self.line_width, command=self.update_line_width)
        line_width_slider.set(self.line_width.get())

        # Pack the buttons and slider
        brush_button.pack(side=tk.LEFT, padx=2, pady=2)
        color_button.pack(side=tk.LEFT, padx=2, pady=2)
        eraser_button.pack(side=tk.LEFT, padx=2, pady=2)
        pencil_button.pack(side=tk.LEFT, padx=2, pady=2)
        clear_button.pack(side=tk.LEFT, padx=2, pady=2)
        save_button.pack(side=tk.LEFT, padx=2, pady=2)
        undo_button.pack(side=tk.LEFT, padx=2, pady=2)
        redo_button.pack(side=tk.LEFT, padx=2, pady=2)
        line_width_slider.pack(side=tk.LEFT, padx=2, pady=2)

    def draw(self, event):
        """Draw on the canvas when the mouse is clicked and moved."""
        current_color = self.drawing_color.get() if self.drawing_tool.get() == BRUSH else BACKGROUND_COLOR
        print("Drawing tool:", self.drawing_tool.get(), "Color:", current_color, "Line width:", self.line_width.get())
        if self.previous_x and self.previous_y:
            if self.drawing_tool.get() == BRUSH:
                line_id = self.canvas.create_oval(event.x - self.line_width.get(), event.y - self.line_width.get(), event.x + self.line_width.get(), event.y + self.line_width.get(), fill=current_color, outline=current_color)
            elif self.drawing_tool.get() == PENCIL:
                line_id = self.canvas.create_line(self.previous_x, self.previous_y, event.x, event.y, width=self.line_width.get(), fill=current_color, capstyle=tk.ROUND, smooth=False)
            else:
                line_id = self.canvas.create_line(self.previous_x, self.previous_y, event.x, event.y, width=self.line_width.get(), fill=current_color, capstyle=tk.ROUND, smooth=True)
            self.undo_stack.append(line_id)
            self.previous_x = event.x
            self.previous_y = event.y

    def reset(self, event):
        """Reset the previous coordinates when the mouse button is released."""
        self.previous_x, self.previous_y = None, None

    def use_brush(self):
        """Set the drawing tool to brush."""
        self.drawing_tool.set(BRUSH)

    def use_eraser(self):
        """Set the drawing tool to eraser."""
        self.drawing_tool.set(ERASER)

    def use_pencil(self):
        """Set the drawing tool to pencil."""
        self.drawing_tool.set(PENCIL)

    def choose_color(self):
        """Open a color chooser dialog and set the drawing color to the selected color."""
        color = colorchooser.askcolor(title="Choose drawing color", initialcolor=self.drawing_color.get())[1]
        if color:
            self.drawing_color.set(color)

    def update_line_width(self, event):
        """Update the line width based on the slider value."""
        self.line_width.set(int(event))

    def clear_canvas(self):
        """Clear the canvas."""
        self.canvas.delete("all")

    def save_drawing(self):
        """Save the drawing as a PNG file."""
        filename = filedialog.asksaveasfilename(title="Save drawing", defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if filename:
            # Use PIL to convert the canvas to an image and save it
            self.canvas.postscript(file="tmp_canvas.eps", colormode="color")
            Image.open("tmp_canvas.eps").convert("RGB").save(filename)

    def undo(self):
        """Undo the last drawing action."""
        if self.undo_stack:
            line_id = self.undo_stack.pop()
            self.canvas.delete(line_id)
            self.redo_stack.append(line_id)

    def redo(self):
        """Redo the last undone drawing action."""
        if self.redo_stack:
            line_id = self.redo_stack.pop()
            self.canvas.itemconfigure(line_id, state="normal")
            self.undo_stack.append(line_id)

    def run(self):
        """Run the main loop."""
        self.window.mainloop()

# Create a DrawingApp instance and run it
if __name__ == "__main__":
    app = DrawingApp()
    app.run()
