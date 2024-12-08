import tkinter as tk


class ScrollableChecklist(tk.Frame):
    def __init__(self, master=None, items=None, **kwargs):
        super().__init__(master, **kwargs)
        self.items = items or []
        self.variables = []

        # Create a canvas and a vertical scrollbar for scrolling
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        # Configure the scrollable frame
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Create a window inside the canvas to host the scrollable frame
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack the canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Add the checkboxes
        self.create_checkboxes()

        # Allow scrolling with the mouse wheel
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def create_checkboxes(self):
        """Create checkboxes for the items."""
        for item in self.items:
            var = tk.BooleanVar(value=False)
            checkbox = tk.Checkbutton(self.scrollable_frame, text=item, variable=var)
            checkbox.pack(anchor="w", padx=5, pady=2)
            self.variables.append(var)

    def get_checked_items(self):
        """Return a list of checked items."""
        return [item for item, var in zip(self.items, self.variables) if var.get()]

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")


# Example usage
if __name__ == "__main__":
    def show_checked_items():
        checked = checklist.get_checked_items()
        print("Checked items:", checked)

    root = tk.Tk()
    root.title("Scrollable Checklist Example")

    # Define some items for the checklist
    items = [f"Item {i + 1}" for i in range(50)]

    # Create the scrollable checklist widget
    checklist = ScrollableChecklist(root, items=items, width=400, height=300)
    checklist.pack(fill="both", expand=True, padx=10, pady=10)

    # Add a button to display selected items
    btn_show = tk.Button(root, text="Show Checked Items", command=show_checked_items)
    btn_show.pack(pady=10)

    root.mainloop()
