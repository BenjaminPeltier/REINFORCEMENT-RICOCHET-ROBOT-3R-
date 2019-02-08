from Board import Board 

class BoardRicochet(Board):

    _conversion = {
        1: "LeftWall",
        2: "RightWall",
        4: "UpWall",
        8: "DownWall",
        16: "Red",
        32: "Blue",
        64: "Green",
        128: "Yellow",
        256: "RedWin",
        512: "BlueWin",
        1024: "GreenWin",
        2048: "YellowWin"
    }


    def __init__(self, xDim, yDim):
        super().__init__(xDim, yDim)


    def _caseTransform(self, x, y): # Ressortir une liste à la place d'un dico
        """
        Can transform a case into a dictionnary
            :param self: The game itself
            :param x: The horizontal position in the board
            :param y: The vertical position in the board
        """
        caseDescr = []
        prev = 0
        current = self.grid.getCase(x, y)
        i = 2048
        while i >= 1 or current == 0:
            prev = current
            current %= i
            if current != prev:
                caseDescr.append(self._conversion[i])
            i // 2
        return caseDescr


    def getCase(self, x, y):
        """
        Get a case of a board at a position (x, y)
            :param self: The board itself
            :param x: The horizontal position of a case
            :param y: The vertical position of a case
            :return: The value of a case
        """
        return self._caseTransform(x, y)


    def setCase(self, x, y, content):  # gérer les listes
        """
        Set the content of a case 
            :param self: The board itself
            :param x: The horizontal position of a case
            :param y: The vertical position of a case
            :param value: The value you want to set (see model description for more informations)
        """
        if type(content) == list:
            value = 0
            for items in content:
                for val, name in self._conversion.items():
                    if(name == items):
                        value += val
        else:
            value = content

        self.grid[y, x] = value


    def findColor(self, color):
        """
        Can find the position of the token of a specific color
            :param self: The board itself
            :param color: The color of the token (string)
            :return: A tuple containing the position of the token
        """
        for x in range(self.grid.getSizeX()):
            for y in range(self.grid.getSizeY()):
                for cat, nb in self.getCase(x, y):
                    if nb and cat==color:
                        return (x, y)
        raise Exception("The token of the desired color doesn't exist")