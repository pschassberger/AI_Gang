import tkinter as tk


class Connect4(tk.Canvas):
    def __init__(self):
        super().__init__(
            width=1080, height=720, background="black", highlightthickness=0
        )

        self.pack()


root = tk.Tk()
root.title("AI Connect 4")
root.resizable(False, False)
root.tk.call("tk", "scaling", 4.0)

board = Connect4()

root.mainloop()


