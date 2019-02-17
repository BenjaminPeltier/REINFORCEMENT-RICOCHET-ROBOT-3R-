from BoardRicochet import BoardRicochet

class Ricochet :
    
    def __init__(self, xDim=16, yDim=16):
        self.grid = BoardRicochet(xDim, yDim)


    def isWin(self):
        """
        True if the player winned, else : false
            :param self: The game itself
        """   
        for x in range(self.grid.getSizeX()):
            for y in range(self.grid.getSizeY()):
                case = self.grid.getCase(x, y)
                if "Red" in case and "RedWin" in case:
                    return True
                elif "Blue" in case and "BlueWin" in case:
                    return True
                elif "Green" in case and "GreenWin" in case:
                    return True
                elif "Yellow" in case and "YellowWin" in case:
                    return True
        return False


    def _move(self, color, vec, blockingWalls):
        """
        Can move a color token following the rules of ricochet in the direction describes by vec
            :param self: The game itself
            :param color: The color of the token
            :param vec: A tuple of shape (movingX, movingY)
            :param blockingWalls: A tuple of shape (blocking wall current case, blocking wall adjacent case)
        """   
        tockenPos = self.grid.findColor(color)
        currentCase = self.grid.getCase(*tockenPos)
        adjCase = self.grid.getCase(tockenPos[0] + vec[0], tockenPos[1] + vec[1])
        nbMoves = 0
        while blockingWalls[0] not in currentCase and blockingWalls[1] not in adjCase and adjCase != None:
            currentCase = adjCase
            nbMoves += 1
            try:
                adjCase = self.grid.getCase(
                    tockenPos[0] + (nbMoves+1)*vec[0], 
                    tockenPos[1] + (nbMoves+1)*vec[1]
                )
            except IndexError:
                adjCase = None
        self.grid.delElements(*tockenPos, color)
        self.grid.addElements(
            tockenPos[0] + (nbMoves)*vec[0], 
            tockenPos[1] + (nbMoves)*vec[1],
            color
        )


    def move(self, color, direction):
        """
        Can move a color token following the rules of ricochet
            :param self: The game itself
            :param color: The color of the token
            :param direction: The movement direction ("left", "right", "up", "low")
        """   
        if direction == "left":
            self._move(color, (-1, 0), ["LeftWall", "RightWall"])
        elif direction == "right":
            self._move(color, (1, 0), ["RightWall", "LeftWall"])
        elif direction == "up":
            self._move(color, (0, -1), ["UpWall", "DownWall"])
        elif direction == "low":
            self._move(color, (0, 1), ["DownWall", "UpWall"])
        else:
            raise Exception("Direction parameter must be equal to 'left', 'right', 'up' or 'low'.")