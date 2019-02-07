import numpy as np

class Board :

    grid = np.zeros((16, 16))

    def __init__(self, *args, **kwargs):
        pass


    def getCase(self, x, y):
        """
        docstring here
            :param self: The board itself
            :param x: The horizontal position of a case
            :param y: The vertical position of a case
            :return: 
        """
        return self.grid[y, x]


    def setCase(self, x, y, value):
        """
        Set the value of a case 
            :param self: The board itself
            :param x: The horizontal position of a case
            :param y: The vertical position of a case
            :param value: The value you want to set (see model description for more informations)
        """
        self.grid[y, x] = value


    def setgrid(self, grid):
        """
        Set the grid
            :param self: The board itself
            :param grid: The matrix grid to set
        """
        self.grid = grid


    def getGrid(self):
        """
        Get the grid
            :param self: The board itself
            :return: The matrix grid
        """
        return self.grid


    def getSizeX(self):
        return self.grid.shape[1]


    def getSizeY(self):
        return self.grid.shape[0]


    def __repr__(self):
        """
        Representation of the board as a vector
            :param self: The board itself
            :return: A numpy array
        """
        return self.grid.reshape(
            (self.grid.shape[0] * self.grid.shape[1])
        )


    def __str__(self):
        """
        Human readable representation of a Board
            :param self: The board itself
        """   
        return self.grid.__str__()
    