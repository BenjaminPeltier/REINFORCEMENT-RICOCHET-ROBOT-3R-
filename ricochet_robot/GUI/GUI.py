import tkinter as tk
from operator import index
from tkinter import Label, mainloop

class Application(tk.Frame):

    def __init__(self, board, master=tk.Tk(), board_width=500, board_height=500, show_grid=True):
        super().__init__(master)
        self.master = master
        self.master.title("Ricochet Robot")

        self.board = board
        self.last_log = tk.StringVar()
        self.last_log.trace("w", self.update)

        self.board_width = board_width
        self.board_height = board_height
        self.show_grid = show_grid

        self.pack()
        self.create_content()


    def create_content(self):
        # Board
        self.canvas = tk.Canvas(self, width=self.board_width, height=self.board_height, bg='white', bd=4, relief="ridge")

        # Logs
        # Frame
        self.logs=tk.Frame(self, width=100, height=500)

        # Logs title
        log_title = tk.Label(self.logs, text="LOGS", width=50)
		
		# Scroll bar
        scroll=tk.Scrollbar(self.logs)

        # Logs text
        self.log_text=tk.Text(self.logs, height=self.board_height//15)  # 15 is the default size of fonts
        self.log_text.configure(yscrollcommand=scroll.set)
        self.log_text.configure(state="disabled")
		
		# Pack everything
        log_title.pack(side="top")
        scroll.pack(side="right")
        self.canvas.pack(side="left")
        self.log_text.pack(side="left")
        self.logs.pack(side="top")


    def update_logs(self):
        self.log_text.configure(state="normal")
        self.log_text.insert("insert", "\n" + str(self.last_log.get()))
        self.log_text.configure(state="disabled")
        self.log_text.pack()
        self.logs.pack()


    def draw_board(self):
        board_x = self.board.size_X()
        board_y = self.board.size_Y()
        width_case = self.board_width // board_x
        height_case = self.board_height // board_y
        start_x = (self.board_width % board_x) // 2 + 7
        start_y = (self.board_height % board_y) // 2 + 7
        margin = 5

        self.canvas.delete("all")

        for x in range(board_x):
            for y in range(board_y):
                for elem in self.board.get_case(x, y):
                    if elem == "LeftWall":
                        self.canvas.create_line(
                            start_x + x * width_case, start_y + y * height_case,
                            start_x + x * width_case, start_y + y * height_case + height_case,
                            width=3,
                            tags="walls"
                        )
                    elif elem == "RightWall":
                        self.canvas.create_line(
                            start_x + x * width_case + width_case, start_y + y * height_case,
                            start_x + x * width_case + width_case, start_y + y * height_case + height_case,
                            width=3,
                            tags="walls"
                        )
                    elif elem == "UpWall":
                        self.canvas.create_line(
                            start_x + x * width_case, start_y + y * height_case,
                            start_x + x * width_case  + width_case, start_y + y * height_case,
                            width=3,
                            tags="walls"
                        )
                    elif elem == "DownWall":
                        self.canvas.create_line(
                            start_x + x * width_case, start_y + y * height_case + height_case,
                            start_x + x * width_case + width_case, start_y + y * height_case + height_case,
                            width=3,
                            tags="walls"
                        )
                    elif elem == "Red":
                        self.canvas.create_oval(
                            start_x + x * width_case + margin, start_y + y * height_case + margin,
                            start_x + x * width_case + width_case - margin, start_y + y * height_case + height_case - margin,
                            width=3,
                            fill="red",
                            outline="red"
                        )
                    elif elem == "Blue":
                        self.canvas.create_oval(
                            start_x + x * width_case + margin, start_y + y * height_case + margin,
                            start_x + x * width_case + width_case - margin, start_y + y * height_case + height_case - margin,
                            width=3,
                            fill="blue",
                            outline="blue"
                        )
                    elif elem == "Green":
                        self.canvas.create_oval(
                            start_x + x * width_case + margin, start_y + y * height_case + margin,
                            start_x + x * width_case + width_case - margin, start_y + y * height_case + height_case - margin,
                            width=3,
                            fill="green",
                            outline="green"
                        )
                    elif elem == "Yellow":
                        self.canvas.create_oval(
                            start_x + x * width_case + margin, start_y + y * height_case + margin,
                            start_x + x * width_case + width_case - margin, start_y + y * height_case + height_case - margin,
                            width=3,
                            fill="yellow",
                            outline="yellow"
                        )
                    elif elem == "RedWin":
                        self.canvas.create_oval(
                            start_x + x * width_case + margin, start_y + y * height_case + margin,
                            start_x + x * width_case + width_case - margin, start_y + y * height_case + height_case - margin,
                            width=3,
                            outline="red"
                        )
                    elif elem == "BlueWin":
                        self.canvas.create_oval(
                            start_x + x * width_case + margin, start_y + y * height_case + margin,
                            start_x + x * width_case + width_case - margin, start_y + y * height_case + height_case - margin,
                            width=3,
                            outline="blue"
                        )
                    elif elem == "GreenWin":
                        self.canvas.create_oval(
                            start_x + x * width_case + margin, start_y + y * height_case + margin,
                            start_x + x * width_case + width_case - margin, start_y + y * height_case + height_case - margin,
                            width=3,
                            outline="green"
                        )
                    elif elem == "YellowWin":
                        self.canvas.create_oval(
                            start_x + x * width_case + margin, start_y + y * height_case + margin,
                            start_x + x * width_case + width_case - margin, start_y + y * height_case + height_case - margin,
                            width=3,
                            outline="yellow"
                        )

                if self.show_grid :
                    self.canvas.create_rectangle(
                        start_x + x * width_case, start_y + y * height_case,
                        start_x + x * width_case + width_case, start_y + y * height_case + height_case,
                        width=1,
                        outline="grey",
                        tags="grid"
                    )
                    self.canvas.tag_lower("grid", "walls")
    

    def update(self, *args):
        self.update_logs()
        self.draw_board()
        self.canvas.pack()
        self.log_text.pack()
        self.logs.pack()
