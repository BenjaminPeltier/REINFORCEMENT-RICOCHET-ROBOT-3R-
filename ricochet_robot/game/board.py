import numpy as np

class Board :

    def __init__(self, dim_x, dim_y):
        self.grid = np.zeros((dim_y, dim_x))


    def load_grid(self, grid_file):
        """
        Load the board grid from a csv
            :param self: The board itself
            :param grid_file: The csv which contains a grid
        """
        with open(grid_file, "rb") as grid:
            self.grid = np.loadtxt(grid, delimiter=",")


    def save_grid(self, grid_file):
        """
        Save the board grid from a csv
            :param self: The board itself
            :param grid_file: The csv which will contain a grid
        """   
        np.savetxt(grid_file, self.grid, delimiter=",")


    def get_case(self, x, y):
        """
        Get a case of a board at a position (x, y)
            :param self: The board itself
            :param x: The horizontal position of a case
            :param y: The vertical position of a case
            :return: The value of a case
        """
        return self.grid[y, x]


    def set_case(self, x, y, value):
        """
        Set the value of a case 
            :param self: The board itself
            :param x: The horizontal position of a case
            :param y: The vertical position of a case
            :param value: The value you want to set (see model description for more informations)
        """
        self.grid[y, x] = value


    def set_grid(self, grid):
        """
        Set the grid
            :param self: The board itself
            :param grid: The matrix grid to set
        """
        self.grid = grid


    def to_mat(self):
        """
        Get the grid in a matrix (numpy array)
            :param self: The board itself
            :return: The matrix grid
        """
        return self.grid


    def size_X(self):
        """
        Get the horizontal size of the board
            :param self: The board itself
        """   
        return self.grid.shape[1]


    def size_Y(self):
        """
        Get the vertical size of the board
            :param self: The board itself
        """   
        return self.grid.shape[0]


    def to_vec(self):
        """
        Transform the board to a vector
            :param self: The board itself
            :return: A vector transformation of the board
        """   
        return self.grid.reshape(
            (self.grid.shape[0] * self.grid.shape[1])
        )


    def __repr__(self):
        """
        Representation of the board as a vector
            :param self: The board itself
            :return: CSV like string
        """
        res = ""
        for line in self.grid:
            for i, nb in enumerate(line):
                res += f"{nb}," if i < self.size_X() - 1 else str(nb)
            res += "\n"
        return res


    def __str__(self):
        """
        Human readable representation of a Board
            :param self: The board itself
        """   
        return str(self.grid)
    