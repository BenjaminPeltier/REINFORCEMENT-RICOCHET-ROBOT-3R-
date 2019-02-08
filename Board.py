import numpy as np

class Board :

    def __init__(self, xDim, yDim):
        self.grid = np.zeros((yDim, xDim))


    def loadGrid(self, gridFile):
        """
        Load the board grid from a csv
            :param self: The board itself
        """   
        self.grid = np.loadtxt(open(gridFile, "rb"), delimiter=",")


    def getCase(self, x, y):
        """
        Get a case of a board at a position (x, y)
            :param self: The board itself
            :param x: The horizontal position of a case
            :param y: The vertical position of a case
            :return: The value of a case
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
        """
        Get the horizontal size of the board
            :param self: The board itself
        """   
        return self.grid.shape[1]


    def getSizeY(self):
        """
        Get the vertical size of the board
            :param self: The board itself
        """   
        return self.grid.shape[0]


    def __repr__(self):
        """
        Representation of the board as a vector
            :param self: The board itself
            :return: A numpy array
        """
        return str(self.grid.reshape(
            (self.grid.shape[0] * self.grid.shape[1])
        ))


    def __str__(self):
        """
        Human readable representation of a Board
            :param self: The board itself
        """   
        return self.grid.__str__()
    