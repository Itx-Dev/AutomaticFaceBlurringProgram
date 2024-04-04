import tkinter as tk
from UserInterface.RenderWidgets import RenderWidgets


class Window:
    def __init__(self):
        self.root = tk.Tk()  # Define Root Window
        self.root.title("Blur Me")  # Set Title
        self.root.geometry("800x500")  # Set Window Size
        self.root.config(bg="skyblue")

        self.mainFrame = tk.Frame(self.root, width=700, height=400, bg="cornsilk2", highlightbackground="black",
                                  highlightthickness=3)

        for i in range(4):
            self.mainFrame.rowconfigure(i, weight=1)
            self.mainFrame.columnconfigure(i, weight=1)

        self.mainFrame.grid_propagate(False)  # Stop frame from shrinking to element's size
        self.mainFrame.pack(anchor="center", expand=True)  # Anchor frame in middle

        RenderWidgets(self.mainFrame)

    # Run Main loop for window
    def runWindow(self):
        self.root.mainloop()
