import numpy as np

class Board :

    grille = np.zeros((16, 16))

    def __init__(self, *args, **kwargs):
        pass

    def getCase(self, x, y):
        pass

    def __repr__(self):
        return self.grille.reshape(
            (self.grille.shape[0] * self.grille.shape[1])
        )

    def __str__(self):
        return self.grille.__str__()
    