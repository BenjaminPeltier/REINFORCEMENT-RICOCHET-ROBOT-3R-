from Board import Board 

class Ricochet :
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

    grid = Board()

    def __init__(self, *args, **kwargs):
        pass


    def _caseTransform(self, x, y):
        """
        docstring here
            :param self: 
            :param x: 
            :param y: 
        """
        caseDescr = {
            "LeftWall": 0, 
            "RightWall": 0, 
            "UpWall": 0, 
            "DownWall": 0, 
            "Red": 0,
            "Blue": 0,
            "Green": 0,
            "Yellow": 0,
            "RedWin": 0,
            "BlueWin": 0,
            "GreenWin": 0,
            "YellowWin": 0,
        }
        prev = 0
        current = self.grid.getCase(x, y)
        i = 2048
        while i >= 1 or current == 0:
            prev = current
            current %= i
            if current != prev:
                caseDescr[self._conversion[i]] = (prev // i)
            i // 2
        return caseDescr


    def isWin(self):
        """
        docstring here
            :param self: 
        """   
        for x in range(self.grid.getSizeX()):
            for y in range(self.grid.getSizeY()):
                caseInfos = self._caseTransform(x, y)
                if caseInfos["Red"] and caseInfos["RedWin"]:
                    return True
                elif caseInfos["Blue"] and caseInfos["BlueWin"]:
                    return True
                elif caseInfos["Green"] and caseInfos["GreenWin"]:
                    return True
                elif caseInfos["Yellow"] and caseInfos["YellowWin"]:
                    return True
        return False
