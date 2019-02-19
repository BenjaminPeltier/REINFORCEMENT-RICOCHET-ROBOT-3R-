import tkinter as tk
from operator import index
from tkinter import Label, mainloop

class Application(tk.Frame):

    def __init__(self, board, master=tk.Tk(), boardWidth=500, boardHeight=500, showGrid=True):
        super().__init__(master)
        self.master = master
        self.master.title("Ricochet Robot")

        self.board = board
        self.lastLog = tk.StringVar()
        self.lastLog.trace("w", self.update)

        self.boardWidth = boardWidth
        self.boardHeight = boardHeight
        self.showGrid = showGrid

        self.pack()
        self.create_content()


    def create_content(self):
        # Board
        self.canvas = tk.Canvas(self, width=self.boardWidth, height=self.boardHeight, bg='white', bd=4, relief="ridge")

        # Logs
        # Frame
        self.logs=tk.Frame(self, width=100, height=500)

        # Logs title
        logTitle = tk.Label(self.logs, text="LOGS", width=50)
		
		# Scroll bar
        scroll=tk.Scrollbar(self.logs)

        # Logs text
        self.logText=tk.Text(self.logs, height=self.boardHeight//15)  # 15 is the default size of fonts
        self.logText.configure(yscrollcommand=scroll.set)
        self.logText.configure(state="disabled")
		
		# Pack everything
        logTitle.pack(side="top")
        scroll.pack(side="right")
        self.canvas.pack(side="left")
        self.logText.pack(side="left")
        self.logs.pack(side="top")


    def updateLogs(self):
        self.logText.configure(state="normal")
        self.logText.insert("insert", "\n" + str(self.lastLog.get()))
        self.logText.configure(state="disabled")
        self.logText.pack()
        self.logs.pack()


    def drawBoard(self):
        boardX = self.board.getSizeX()
        boardY = self.board.getSizeY()
        widthCase = self.boardWidth // boardX
        heightCase = self.boardHeight // boardY
        startX = (self.boardWidth % boardX) // 2 + 7
        startY = (self.boardHeight % boardY) // 2 + 7
        margin = 5

        self.canvas.delete("all")

        for x in range(boardX):
            for y in range(boardY):
                for elem in self.board.getCase(x, y):
                    if elem == "LeftWall":
                        self.canvas.create_line(
                            startX + x * widthCase, startY + y * heightCase,
                            startX + x * widthCase, startY + y * heightCase + heightCase,
                            width=3,
                            tags="walls"
                        )
                    elif elem == "RightWall":
                        self.canvas.create_line(
                            startX + x * widthCase + widthCase, startY + y * heightCase,
                            startX + x * widthCase + widthCase, startY + y * heightCase + heightCase,
                            width=3,
                            tags="walls"
                        )
                    elif elem == "UpWall":
                        self.canvas.create_line(
                            startX + x * widthCase, startY + y * heightCase,
                            startX + x * widthCase  + widthCase, startY + y * heightCase,
                            width=3,
                            tags="walls"
                        )
                    elif elem == "DownWall":
                        self.canvas.create_line(
                            startX + x * widthCase, startY + y * heightCase + heightCase,
                            startX + x * widthCase + widthCase, startY + y * heightCase + heightCase,
                            width=3,
                            tags="walls"
                        )
                    elif elem == "Red":
                        self.canvas.create_oval(
                            startX + x * widthCase + margin, startY + y * heightCase + margin,
                            startX + x * widthCase + widthCase - margin, startY + y * heightCase + heightCase - margin,
                            width=3,
                            fill="red",
                            outline="red"
                        )
                    elif elem == "Blue":
                        self.canvas.create_oval(
                            startX + x * widthCase + margin, startY + y * heightCase + margin,
                            startX + x * widthCase + widthCase - margin, startY + y * heightCase + heightCase - margin,
                            width=3,
                            fill="blue",
                            outline="blue"
                        )
                    elif elem == "Green":
                        self.canvas.create_oval(
                            startX + x * widthCase + margin, startY + y * heightCase + margin,
                            startX + x * widthCase + widthCase - margin, startY + y * heightCase + heightCase - margin,
                            width=3,
                            fill="green",
                            outline="green"
                        )
                    elif elem == "Yellow":
                        self.canvas.create_oval(
                            startX + x * widthCase + margin, startY + y * heightCase + margin,
                            startX + x * widthCase + widthCase - margin, startY + y * heightCase + heightCase - margin,
                            width=3,
                            fill="yellow",
                            outline="yellow"
                        )
                    elif elem == "RedWin":
                        self.canvas.create_oval(
                            startX + x * widthCase + margin, startY + y * heightCase + margin,
                            startX + x * widthCase + widthCase - margin, startY + y * heightCase + heightCase - margin,
                            width=3,
                            outline="red"
                        )
                    elif elem == "BlueWin":
                        self.canvas.create_oval(
                            startX + x * widthCase + margin, startY + y * heightCase + margin,
                            startX + x * widthCase + widthCase - margin, startY + y * heightCase + heightCase - margin,
                            width=3,
                            outline="blue"
                        )
                    elif elem == "GreenWin":
                        self.canvas.create_oval(
                            startX + x * widthCase + margin, startY + y * heightCase + margin,
                            startX + x * widthCase + widthCase - margin, startY + y * heightCase + heightCase - margin,
                            width=3,
                            outline="green"
                        )
                    elif elem == "YellowWin":
                        self.canvas.create_oval(
                            startX + x * widthCase + margin, startY + y * heightCase + margin,
                            startX + x * widthCase + widthCase - margin, startY + y * heightCase + heightCase - margin,
                            width=3,
                            outline="yellow"
                        )

                if self.showGrid :
                    self.canvas.create_rectangle(
                        startX + x * widthCase, startY + y * heightCase,
                        startX + x * widthCase + widthCase, startY + y * heightCase + heightCase,
                        width=1,
                        outline="grey",
                        tags="grid"
                    )
                    self.canvas.tag_lower("grid", "walls")
    

    def update(self, *args):
        self.updateLogs()
        self.drawBoard()
        self.canvas.pack()
        self.logText.pack()
        self.logs.pack()
