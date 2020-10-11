import tkinter as tk


class Connect4(tk.Canvas):
    def __init__(self):
        super().__init__(
            width=1080, height=720, background="black", highlightthickness=0
        )
        
        self.agents()
        self.grid()

        self.pack()

    def grid

    def agents(self, x, y, agent):
        if agent == 0:
            self.create_oval(x, y, 80, 80,  
                        outline = "black", fill = "yellow", 
                        width = 2)
        if agent == 1:
            self.create_oval(x, y, 80, 80,  
                        outline = "black", fill = "blue", 
                        width = 2) 


root = tk.Tk()
root.title("AI Connect 4")
root.resizable(False, False)
root.tk.call("tk", "scaling", 4.0)

board = Connect4()

root.mainloop()


